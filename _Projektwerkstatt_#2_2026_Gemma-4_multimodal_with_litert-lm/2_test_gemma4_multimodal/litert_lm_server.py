import base64
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any

import litert_lm
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


MODEL_PATH = os.getenv("LITERT_MODEL_PATH", "./gemma-4-E4B-it.litertlm")
LITERT_BACKEND = os.getenv("LITERT_BACKEND", "CPU").upper()
LITERT_AUDIO_BACKEND = os.getenv("LITERT_AUDIO_BACKEND", "CPU").upper()

app = FastAPI(title="LiteRT-LM OpenAI-compatible local API")

engine = None


class ChatRequest(BaseModel):
    model: str | None = None
    messages: list[dict[str, Any]]
    stream: bool = False
    max_tokens: int | None = None
    temperature: float | None = None


def pick_backend(name: str):
    if name == "GPU":
        return litert_lm.Backend.GPU
    if name == "NPU":
        return litert_lm.Backend.NPU
    return litert_lm.Backend.CPU


def model_name() -> str:
    return Path(MODEL_PATH).stem


def suffix_from_data_url(data_url: str, fallback: str) -> str:
    header = data_url.split(",", 1)[0].lower()

    if "image/jpeg" in header:
        return ".jpg"
    if "image/png" in header:
        return ".png"
    if "image/gif" in header:
        return ".gif"
    if "image/bmp" in header:
        return ".bmp"

    if "audio/wav" in header or "audio/x-wav" in header:
        return ".wav"
    if "audio/mpeg" in header or "audio/mp3" in header:
        return ".mp3"
    if "audio/mp4" in header:
        return ".m4a"
    if "audio/ogg" in header:
        return ".ogg"
    if "audio/flac" in header:
        return ".flac"
    if "audio/webm" in header:
        return ".webm"

    return fallback


def data_url_to_temp_file(data_url: str, fallback_suffix: str) -> str:
    if "," not in data_url:
        raise ValueError("Invalid data URL.")

    _, b64 = data_url.split(",", 1)
    raw = base64.b64decode(b64)
    suffix = suffix_from_data_url(data_url, fallback_suffix)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(raw)
    tmp.close()

    return tmp.name


def openai_part_to_litert(
    part: dict[str, Any],
    temp_files: list[str],
) -> dict[str, Any]:
    part_type = part.get("type")

    if part_type == "text":
        return {
            "type": "text",
            "text": part.get("text", ""),
        }

    if part_type == "image_url":
        url = part.get("image_url", {}).get("url", "")

        if not url:
            raise ValueError("Missing image_url.url")

        if url.startswith("data:"):
            path = data_url_to_temp_file(url, ".jpg")
            temp_files.append(path)
            return {
                "type": "image",
                "path": path,
            }

        return {
            "type": "image",
            "path": url,
        }

    if part_type == "audio_url":
        url = part.get("audio_url", {}).get("url", "")

        if not url:
            raise ValueError("Missing audio_url.url")

        if url.startswith("data:"):
            path = data_url_to_temp_file(url, ".wav")
            temp_files.append(path)
            return {
                "type": "audio",
                "path": path,
            }

        return {
            "type": "audio",
            "path": url,
        }

    raise ValueError(f"Unsupported content part type: {part_type}")


def openai_message_to_litert(
    message: dict[str, Any],
    temp_files: list[str],
) -> dict[str, Any]:
    role = message.get("role", "user")
    content = message.get("content", "")

    if isinstance(content, str):
        return {
            "role": role,
            "content": content,
        }

    if isinstance(content, list):
        return {
            "role": role,
            "content": [
                openai_part_to_litert(part, temp_files)
                for part in content
            ],
        }

    return {
        "role": role,
        "content": str(content),
    }


def extract_text(response: Any) -> str:
    """
    LiteRT-LM response objects can vary slightly between versions.
    This function keeps extraction defensive.
    """
    if response is None:
        return ""

    if isinstance(response, str):
        return response

    if isinstance(response, dict):
        content = response.get("content", response)

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            chunks = []

            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        chunks.append(item.get("text", ""))
                    elif "text" in item:
                        chunks.append(str(item["text"]))
                elif isinstance(item, str):
                    chunks.append(item)

            return "".join(chunks)

        if "text" in response:
            return str(response["text"])

    if hasattr(response, "text"):
        return str(response.text)

    if hasattr(response, "content"):
        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            chunks = []

            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        chunks.append(item.get("text", ""))
                    elif "text" in item:
                        chunks.append(str(item["text"]))
                elif isinstance(item, str):
                    chunks.append(item)

            return "".join(chunks)

    return str(response)


def cleanup_temp_files(temp_files: list[str]) -> None:
    for file_path in temp_files:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except OSError:
            pass


def make_stream_chunk(
    text: str,
    created: int,
    finish_reason: str | None = None,
) -> str:
    payload = {
        "id": f"chatcmpl-litert-{created}",
        "object": "chat.completion.chunk",
        "created": created,
        "model": model_name(),
        "choices": [
            {
                "index": 0,
                "delta": {"content": text} if text else {},
                "finish_reason": finish_reason,
            }
        ],
    }

    return f"data: {json.dumps(payload)}\n\n"


@app.on_event("startup")
def startup():
    global engine

    if not Path(MODEL_PATH).exists():
        raise FileNotFoundError(
            f"LiteRT-LM model not found: {MODEL_PATH}. "
            "Set LITERT_MODEL_PATH or place the .litertlm file there."
        )

    litert_lm.set_min_log_severity(litert_lm.LogSeverity.ERROR)

    backend = pick_backend(LITERT_BACKEND)
    audio_backend = pick_backend(LITERT_AUDIO_BACKEND)

    try:
        engine = litert_lm.Engine(
            MODEL_PATH,
            backend=backend,
            vision_backend=backend,
            audio_backend=audio_backend,
        )
    except RuntimeError as e:
        if "Vision Encoder model must have exactly one signature" in str(e):
            print("Vision backend failed; falling back to text/audio-less mode: {e}")
            engine = litert_lm.Engine(
                MODEL_PATH,
                backend=backend,
            )
        else:
            raise

    print(f"LiteRT-LM loaded: {MODEL_PATH}")
    print(f"Backend: {LITERT_BACKEND}")
    print(f"Audio backend: {LITERT_AUDIO_BACKEND}")


@app.on_event("shutdown")
def shutdown():
    global engine

    if engine is not None:
        engine.close()
        engine = None


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": model_name(),
        "model_path": MODEL_PATH,
        "backend": LITERT_BACKEND,
        "audio_backend": LITERT_AUDIO_BACKEND,
        "engine_loaded": engine is not None,
    }


@app.get("/v1/models")
def list_models():
    created = int(time.time())

    return {
        "object": "list",
        "data": [
            {
                "id": model_name(),
                "object": "model",
                "created": created,
                "owned_by": "local",
            }
        ],
    }


@app.post("/v1/chat/completions")
def chat_completions(req: ChatRequest):
    if engine is None:
        raise HTTPException(
            status_code=503,
            detail="LiteRT-LM engine is not initialized.",
        )

    if not req.messages:
        raise HTTPException(
            status_code=400,
            detail="Request must contain at least one message.",
        )

    temp_files: list[str] = []

    try:
        litert_messages = [
            openai_message_to_litert(message, temp_files)
            for message in req.messages
        ]
    except Exception as e:
        cleanup_temp_files(temp_files)
        raise HTTPException(
            status_code=400,
            detail=f"Invalid message format: {e}",
        ) from e

    created = int(time.time())
    request_model_name = req.model or model_name()

    if req.stream:
        def event_stream():
            try:
                with engine.create_conversation() as conversation:
                    # Replay history synchronously.
                    # This should be text-only history from the frontend.
                    for history_message in litert_messages[:-1]:
                        conversation.send_message(history_message)

                    # Stream only the newest user turn.
                    last_message = litert_messages[-1]

                    if hasattr(conversation, "send_message_async"):
                        response_stream = conversation.send_message_async(last_message)

                        for chunk in response_stream:
                            text_piece = extract_text(chunk)

                            if text_piece:
                                payload = {
                                    "id": f"chatcmpl-litert-{created}",
                                    "object": "chat.completion.chunk",
                                    "created": created,
                                    "model": request_model_name,
                                    "choices": [
                                        {
                                            "index": 0,
                                            "delta": {"content": text_piece},
                                            "finish_reason": None,
                                        }
                                    ],
                                }

                                yield f"data: {json.dumps(payload)}\n\n"
                    else:
                        # Fallback for older LiteRT-LM versions.
                        response = conversation.send_message(last_message)
                        text = extract_text(response)

                        if text:
                            yield make_stream_chunk(
                                text=text,
                                created=created,
                                finish_reason=None,
                            )

                done_payload = {
                    "id": f"chatcmpl-litert-{created}",
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": request_model_name,
                    "choices": [
                        {
                            "index": 0,
                            "delta": {},
                            "finish_reason": "stop",
                        }
                    ],
                }

                yield f"data: {json.dumps(done_payload)}\n\n"
                yield "data: [DONE]\n\n"

            except Exception as e:
                error_payload = {
                    "error": {
                        "message": str(e),
                        "type": "litert_lm_error",
                    }
                }
                yield f"data: {json.dumps(error_payload)}\n\n"
                yield "data: [DONE]\n\n"

            finally:
                cleanup_temp_files(temp_files)

        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
        )

    try:
        with engine.create_conversation() as conversation:
            response = None

            for message in litert_messages:
                response = conversation.send_message(message)

        text = extract_text(response)

        return {
            "id": f"chatcmpl-litert-{created}",
            "object": "chat.completion",
            "created": created,
            "model": request_model_name,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": text,
                    },
                    "finish_reason": "stop",
                }
            ],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LiteRT-LM generation failed: {e}",
        ) from e

    finally:
        cleanup_temp_files(temp_files)
import base64
import os
import textwrap
from pathlib import Path
from typing import Any

import gradio as gr
from openai import OpenAI


DEFAULT_BASE_URL = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:8000/v1")
DEFAULT_MODEL = os.getenv("LOCAL_LLM_MODEL", "gemma-4-E4B-it")
DEFAULT_API_KEY = os.getenv("LOCAL_LLM_API_KEY", "EMPTY")

# Keep only the last N text turns in context.
# This avoids replaying an ever-growing prompt through LiteRT-LM.
MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS", "6"))
MAX_HISTORY_CHARS = int(os.getenv("MAX_HISTORY_CHARS", "12000"))
SUMMARY_TRIGGER_CHARS = int(os.getenv("SUMMARY_TRIGGER_CHARS", "9000"))
SUMMARY_MAX_CHARS = int(os.getenv("SUMMARY_MAX_CHARS", "1200"))
MAX_MEDIA_FILE_MB = int(os.getenv("MAX_MEDIA_FILE_MB", "12"))

# When image/audio is uploaded, ask the model to include a compact textual
# summary in its answer. That summary remains in the visible chat history and
# can be used in follow-up turns without resending the original media.
MEDIA_CONTEXT_SUMMARY = os.getenv("MEDIA_CONTEXT_SUMMARY", "true").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

client = OpenAI(
    base_url=DEFAULT_BASE_URL,
    api_key=DEFAULT_API_KEY,
)


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"}

MIME_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".webm": "audio/webm",
}


def extract_file_path(file_item: Any) -> str:
    """
    Gradio may return uploaded files as strings, dictionaries,
    or FileData-like objects depending on the version.
    This normalizes all cases to a local file path.
    """
    if isinstance(file_item, str):
        return file_item

    if isinstance(file_item, dict):
        return (
            file_item.get("path")
            or file_item.get("name")
            or file_item.get("file", {}).get("path")
            or ""
        )

    return getattr(file_item, "path", None) or getattr(file_item, "name", "") or ""


def file_to_data_url(file_path: str) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()

    mime = MIME_MAP.get(ext)
    if not mime:
        raise ValueError(f"Unsupported file type: {ext}")

    with path.open("rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime};base64,{encoded}"


def get_file_kind(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()

    if ext == ".webp":
        raise ValueError("WebP is not supported. Use JPG, PNG, GIF, or BMP.")

    if ext in IMAGE_EXTENSIONS:
        return "image"

    if ext in AUDIO_EXTENSIONS:
        return "audio"

    supported = ", ".join(sorted(IMAGE_EXTENSIONS | AUDIO_EXTENSIONS))
    raise ValueError(f"Unsupported file type: {ext}. Supported: {supported}")


def content_part_from_file(file_path: str) -> dict[str, Any]:
    kind = get_file_kind(file_path)

    if kind == "image":
        return {
            "type": "image_url",
            "image_url": {"url": file_to_data_url(file_path)},
        }

    if kind == "audio":
        return {
            "type": "audio_url",
            "audio_url": {"url": file_to_data_url(file_path)},
        }

    raise ValueError(f"Unsupported file: {file_path}")


def build_media_context_instruction(
    text: str,
    image_count: int,
    audio_count: int,
) -> str:
    """
    This instruction is sent only in the current multimodal turn.
    The actual media data is not resent in later turns.
    The model's answer should contain enough textual context for follow-up questions.
    """
    if not MEDIA_CONTEXT_SUMMARY:
        return text

    if image_count == 0 and audio_count == 0:
        return text

    media_parts = []

    if image_count:
        media_parts.append(f"{image_count} image(s)")

    if audio_count:
        media_parts.append(f"{audio_count} audio file(s)")

    media_description = " and ".join(media_parts)

    instruction = (
        f"\n\nYou are receiving {media_description} in this message. "
        "Use the media directly to answer the user. "
        "You can analyze both images and audio provided in this turn. "
        "Also include a short, useful textual summary of the media in your answer "
        "so that future follow-up questions can rely on the text chat history "
        "without resending the original media. "
        "Keep this summary concise and natural."
    )

    if audio_count:
        instruction += (
            "If audio contains speech, transcribe it first. Answer to the respective content of the audio!"
            "If no speech is present, briefly describe what is audible instead."
        )

    if text:
        return text + instruction

    if audio_count and image_count == 0:
        return (
            "Transcribe the audio. If no speech is present, briefly explain what is audible instead."
            + instruction
        )

    return (
        f"Please analyze the attached {media_description}."
        + instruction
    )


def build_user_content(text: str, files: list[Any]) -> str | list[dict[str, Any]]:
    content: list[dict[str, Any]] = []
    image_count = 0
    audio_count = 0

    for file_item in files or []:
        file_path = extract_file_path(file_item)

        if not file_path:
            continue

        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > MAX_MEDIA_FILE_MB:
            raise ValueError(
                f"File too large: {Path(file_path).name} ({file_size_mb:.1f} MB). "
                f"Limit is {MAX_MEDIA_FILE_MB} MB."
            )

        kind = get_file_kind(file_path)

        if kind == "image":
            image_count += 1
        elif kind == "audio":
            audio_count += 1

        content.append(content_part_from_file(file_path))

    text_with_media_instruction = build_media_context_instruction(
        text=text,
        image_count=image_count,
        audio_count=audio_count,
    )

    if text_with_media_instruction:
        content.append(
            {
                "type": "text",
                "text": text_with_media_instruction,
            }
        )

    if not content:
        return ""

    # For text-only messages, keep content as a plain string.
    # For image/audio messages, use OpenAI-compatible multimodal content blocks.
    if len(content) == 1 and content[0]["type"] == "text":
        return content[0]["text"]

    return content


def stringify_history_item(item: Any) -> str:
    """
    Converts Gradio history entries into text only.
    This intentionally drops any previous file/media data.
    """
    if item is None:
        return ""

    if isinstance(item, str):
        return item.strip()

    if isinstance(item, dict):
        # MultimodalTextbox may store user entries like:
        # {"text": "...", "files": [...]}
        text = item.get("text", "")

        if text:
            return str(text).strip()

        content = item.get("content", "")

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            text_parts = []

            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    part_text = part.get("text", "")
                    if part_text:
                        text_parts.append(str(part_text))

            return "\n".join(text_parts).strip()

        return ""

    if isinstance(item, (list, tuple)):
        text_parts = []

        for sub_item in item:
            sub_text = stringify_history_item(sub_item)
            if sub_text:
                text_parts.append(sub_text)

        return "\n".join(text_parts).strip()

    return str(item).strip()


def normalize_history(history: list[Any]) -> list[dict[str, str]]:
    """
    Supports the classic Gradio ChatInterface history format:

        [
            (user_message, assistant_message),
            ...
        ]

    It also tolerates dict-style messages if Gradio returns them in some versions.

    Important:
    - Only text is kept.
    - Old image/audio data is never resent.
    - History is capped to MAX_HISTORY_TURNS.
    """
    messages: list[dict[str, str]] = []

    if not history:
        return messages

    recent_history = history[-MAX_HISTORY_TURNS:]

    for item in recent_history:
        # Classic format: (user_message, assistant_message)
        if isinstance(item, (list, tuple)) and len(item) == 2:
            user_msg, assistant_msg = item

            user_text = stringify_history_item(user_msg)
            assistant_text = stringify_history_item(assistant_msg)

            if user_text:
                messages.append({"role": "user", "content": user_text})

            if assistant_text:
                messages.append({"role": "assistant", "content": assistant_text})

            continue

        # Dict-style fallback.
        if isinstance(item, dict):
            role = item.get("role")
            content = stringify_history_item(item.get("content", ""))

            if role in {"user", "assistant", "system"} and content:
                messages.append({"role": role, "content": content})

    return messages


def estimate_messages_chars(messages: list[dict[str, Any]]) -> int:
    total = 0
    for message in messages:
        content = message.get("content", "")
        if isinstance(content, str):
            total += len(content)
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    total += len(str(part.get("text", "")))
    return total


def summarize_older_history(messages: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for msg in messages:
        role = msg.get("role", "user")
        role_prefix = "User" if role == "user" else "Assistant"
        text = " ".join(msg.get("content", "").split())
        if not text:
            continue
        lines.append(f"{role_prefix}: {textwrap.shorten(text, width=220, placeholder='...')}")

    summary = "\n".join(lines)
    if len(summary) > SUMMARY_MAX_CHARS:
        summary = summary[: SUMMARY_MAX_CHARS - 3] + "..."
    return summary


def compact_history_for_budget(history_messages: list[dict[str, str]]) -> list[dict[str, str]]:
    if not history_messages:
        return history_messages

    total_chars = sum(len(msg.get("content", "")) for msg in history_messages)
    if total_chars <= SUMMARY_TRIGGER_CHARS:
        return history_messages

    keep_tail = 6
    older = history_messages[:-keep_tail]
    tail = history_messages[-keep_tail:]

    compacted: list[dict[str, str]] = tail
    if older:
        summary = summarize_older_history(older)
        if summary:
            compacted = [
                {
                    "role": "system",
                    "content": (
                        "Conversation summary of earlier turns. "
                        "Use this as context and prioritize newer turns if conflicts exist:\n"
                        f"{summary}"
                    ),
                }
            ] + tail

    while compacted and estimate_messages_chars(compacted) > MAX_HISTORY_CHARS:
        if len(compacted) <= 2:
            break
        drop_index = 1 if compacted[0].get("role") == "system" else 0
        compacted.pop(drop_index)

    return compacted


def chat(message: dict[str, Any], history: list[Any], request: gr.Request):
    text = (message or {}).get("text", "") or ""
    files = (message or {}).get("files", []) or []

    if not text and not files:
        yield "⚠️ Please enter a message or upload a file."
        return

    try:
        user_content = build_user_content(text, files)
    except ValueError as e:
        yield f"⚠️ {e}"
        return

    messages = compact_history_for_budget(normalize_history(history))
    messages.append({"role": "user", "content": user_content})

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            stream=True,
            extra_body={"session_id": getattr(request, "session_hash", None)},
        )

        partial = ""

        for chunk in response:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta.content:
                partial += delta.content
                yield partial

    except Exception as e:
        yield (
            "Error connecting to LiteRT-LM server\n\n"
            f"Endpoint: {DEFAULT_BASE_URL}\n"
            f"Model: {DEFAULT_MODEL}\n\n"
            f"{e}"
        )


demo = gr.ChatInterface(
    fn=chat,
    title="Local AI Chat",
    description=(
        "LiteRT-LM backend with Gemma 4 multimodal support. "
        "Images and audio are only sent in the current turn; later turns use text history."
    ),
    multimodal=True,
    textbox=gr.MultimodalTextbox(
        file_count="multiple",
        file_types=["image", "audio"],
        sources=["upload", "microphone"],
        placeholder="Type a message, upload image/audio, or use mic...",
        show_label=False,
    ),
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")

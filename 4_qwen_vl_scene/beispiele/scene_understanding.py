"""Scene Understanding with Qwen VL.

This example shows how to analyze images using qwen3-vl locally with Ollama
or via the KIARA API.
"""

import base64
import mimetypes
import os
from pathlib import Path
from typing import Dict, List, Optional

import ollama
import requests
from dotenv import load_dotenv

load_dotenv(override=False)


def encode_image_base64(image_path: str) -> str:
    """Encode image to base64 for Ollama.

    Args:
        image_path: Path to image file

    Returns:
        Base64 encoded image
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def encode_image_data_url(image_path: str) -> str:
    """Encode image as a data URL for API usage."""
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg"
    encoded = encode_image_base64(image_path)
    return f"data:{mime_type};base64,{encoded}"


def analyze_image_ollama(
    image_path: str,
    prompt: str = "Describe what's in this image in detail.",
    model: str = "qwen3.5:0.8b",
) -> str:
    """Analyze an image using qwen3.5:0.8B (newest unified LLM/VLM, see: https://ollama.com/library/qwen3.5) with Ollama.

    Args:
        image_path: Path to image file
        prompt: Question about the image
        model: Ollama model to use

    Returns:
        Model's response
    """
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [encode_image_base64(image_path)],
            }
        ],
    )

    return response["message"]["content"]


def analyze_image_kiara(
    image_path: str,
    prompt: str = "Describe what's in this image in detail.",
    model: str = "qwen3-vl-30b-a3b-instruct",
    api_base: Optional[str] = None,
) -> str:
    """Analyze an image using qwen3-vl via the KIARA API."""
    api_key = os.getenv("KIARA_API_KEY")
    if not api_key:
        raise ValueError("KIARA_API_KEY is not set in the environment.")

    base = (
        api_base
        or os.getenv("KIARA_API_BASE", "https://kiara.sc.uni-leipzig.de/api/v1")
    ).rstrip("/")
    url = f"{base}/chat/completions"
    data_url = encode_image_data_url(image_path)

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
    }

    response = requests.post(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def analyze_image(
    image_path: str,
    prompt: str = "Describe what's in this image in detail.",
    model: str = "qwen3.5:0.8b",
    backend: str = "ollama",
    kiara_model: str = "qwen3-vl-30b-a3b-instruct",
    api_base: Optional[str] = None,
) -> str:
    """Analyze an image using Ollama or KIARA."""
    if backend == "ollama":
        return analyze_image_ollama(image_path, prompt, model)
    if backend == "kiara":
        return analyze_image_kiara(image_path, prompt, kiara_model, api_base)
    raise ValueError("Unsupported backend. Use 'ollama' or 'kiara'.")


def detect_objects(
    image_path: str,
    model: str = "qwen3.5:0.8b",
    backend: str = "ollama",
    kiara_model: str = "qwen3-vl-30b-a3b-instruct",
) -> List[str]:
    """Detect objects in an image.

    Args:
        image_path: Path to image file
        model: Ollama model to use
        backend: Backend to use (ollama or kiara)
        kiara_model: KIARA model to use

    Returns:
        List of detected objects
    """
    prompt = """List all distinct objects visible in this image.
Provide a simple list, one item per line.
Do not add explanations or descriptions."""

    response = analyze_image(
        image_path,
        prompt,
        model=model,
        backend=backend,
        kiara_model=kiara_model,
    )

    objects = [line.strip() for line in response.strip().split("\n") if line.strip()]
    return objects


def describe_scene(
    image_path: str,
    model: str = "qwen3.5:0.8b",
    backend: str = "ollama",
    kiara_model: str = "qwen3-vl-30b-a3b-instruct",
) -> Dict[str, str]:
    """Get a structured scene description.

    Args:
        image_path: Path to image file
        model: Ollama model to use
        backend: Backend to use (ollama or kiara)
        kiara_model: KIARA model to use

    Returns:
        Dictionary with scene details
    """
    prompt = """Analyze this image and provide:
1. Main subject: What is the main focus?
2. Environment: Where is this taking place?
3. Mood: What atmosphere or feeling does it convey?
4. Colors: What are the dominant colors?

Format as simple bullet points."""

    response = analyze_image(
        image_path,
        prompt,
        model=model,
        backend=backend,
        kiara_model=kiara_model,
    )

    result = {
        "description": response,
        "image_path": image_path,
        "model": model,
    }

    return result


def interactive_analysis(
    image_path: str,
    model: str = "qwen3.5:0.8b",
    backend: str = "ollama",
    kiara_model: str = "qwen3-vl-30b-a3b-instruct",
    api_base: Optional[str] = None,
) -> None:
    """Run interactive image analysis.

    Args:
        image_path: Path to image file
    """
    print(f"Analyzing: {image_path}")
    print("=" * 50)

    print("\n1. Basic Description:")
    print("-" * 30)
    desc = analyze_image(
        image_path,
        "Provide a brief description of what's in this image.",
        model=model,
        backend=backend,
        kiara_model=kiara_model,
        api_base=api_base,
    )
    print(desc)

    print("\n2. Object Detection:")
    print("-" * 30)
    objects = detect_objects(
        image_path,
        model=model,
        backend=backend,
        kiara_model=kiara_model,
    )
    for obj in objects:
        print(f"  - {obj}")

    print("\n3. Scene Analysis:")
    print("-" * 30)
    scene = describe_scene(
        image_path,
        model=model,
        backend=backend,
        kiara_model=kiara_model,
    )
    print(scene["description"])

    print("\n" + "=" * 50)


def main() -> None:
    """Run scene understanding examples."""
    import argparse

    parser = argparse.ArgumentParser(description="Scene Understanding with Qwen VL")
    parser.add_argument("image", help="Path to image file")
    parser.add_argument(
        "--prompt", default="Describe what's in this image.", help="Custom prompt"
    )
    parser.add_argument(
        "--backend",
        default="ollama",
        choices=["ollama", "kiara"],
        help="Backend to use",
    )
    parser.add_argument("--model", default="qwen3.5:0.8b", help="Ollama model to use")
    parser.add_argument(
        "--kiara-model",
        default="qwen3-vl-30b-a3b-instruct",
        help="KIARA model to use",
    )
    parser.add_argument(
        "--kiara-api-base",
        default=None,
        help="Override KIARA API base URL",
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Run interactive analysis"
    )

    args = parser.parse_args()

    if not Path(args.image).exists():
        print(f"Error: Image not found: {args.image}")
        return

    if args.interactive:
        interactive_analysis(
            args.image,
            model=args.model,
            backend=args.backend,
            kiara_model=args.kiara_model,
            api_base=args.kiara_api_base,
        )
    else:
        result = analyze_image(
            args.image,
            args.prompt,
            model=args.model,
            backend=args.backend,
            kiara_model=args.kiara_model,
            api_base=args.kiara_api_base,
        )
        print(result)


if __name__ == "__main__":
    main()

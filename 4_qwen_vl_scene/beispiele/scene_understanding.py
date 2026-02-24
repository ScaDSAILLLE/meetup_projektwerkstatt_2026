"""Scene Understanding with Qwen VL.

This example shows how to analyze images using qwen3-vl:2b with Ollama.
"""

import base64
import ollama
from pathlib import Path
from typing import Dict, List, Optional


def encode_image(image_path: str) -> str:
    """Encode image to base64 for Ollama.

    Args:
        image_path: Path to image file

    Returns:
        Base64 encoded image
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_image(
    image_path: str,
    prompt: str = "Describe what's in this image in detail.",
    model: str = "qwen3-vl:2b",
) -> str:
    """Analyze an image using qwen3-vl.

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
                "images": [encode_image(image_path)],
            }
        ],
    )

    return response["message"]["content"]


def detect_objects(
    image_path: str,
    model: str = "qwen3-vl:2b",
) -> List[str]:
    """Detect objects in an image.

    Args:
        image_path: Path to image file
        model: Ollama model to use

    Returns:
        List of detected objects
    """
    prompt = """List all distinct objects visible in this image.
Provide a simple list, one item per line.
Do not add explanations or descriptions."""

    response = analyze_image(image_path, prompt, model)

    objects = [line.strip() for line in response.strip().split("\n") if line.strip()]
    return objects


def describe_scene(
    image_path: str,
    model: str = "qwen3-vl:2b",
) -> Dict[str, str]:
    """Get a structured scene description.

    Args:
        image_path: Path to image file
        model: Ollama model to use

    Returns:
        Dictionary with scene details
    """
    prompt = """Analyze this image and provide:
1. Main subject: What is the main focus?
2. Environment: Where is this taking place?
3. Mood: What atmosphere or feeling does it convey?
4. Colors: What are the dominant colors?

Format as simple bullet points."""

    response = analyze_image(image_path, prompt, model)

    result = {
        "description": response,
        "image_path": image_path,
        "model": model,
    }

    return result


def interactive_analysis(image_path: str) -> None:
    """Run interactive image analysis.

    Args:
        image_path: Path to image file
    """
    print(f"Analyzing: {image_path}")
    print("=" * 50)

    print("\n1. Basic Description:")
    print("-" * 30)
    desc = analyze_image(
        image_path, "Provide a brief description of what's in this image."
    )
    print(desc)

    print("\n2. Object Detection:")
    print("-" * 30)
    objects = detect_objects(image_path)
    for obj in objects:
        print(f"  - {obj}")

    print("\n3. Scene Analysis:")
    print("-" * 30)
    scene = describe_scene(image_path)
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
    parser.add_argument("--model", default="qwen3-vl:2b", help="Ollama model to use")
    parser.add_argument(
        "--interactive", action="store_true", help="Run interactive analysis"
    )

    args = parser.parse_args()

    if not Path(args.image).exists():
        print(f"Error: Image not found: {args.image}")
        return

    if args.interactive:
        interactive_analysis(args.image)
    else:
        result = analyze_image(args.image, args.prompt, args.model)
        print(result)


if __name__ == "__main__":
    main()

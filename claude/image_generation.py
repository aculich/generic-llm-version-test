#!/usr/bin/env python3
"""
Script to generate images using OpenAI DALL-E, Google Imagen, and Stability AI.

Requirements:
    pip install openai google-genai requests

Environment variables:
    OPENAI_API_KEY - OpenAI API key
    GEMINI_API_KEY - Google AI API key
    STABILITY_API_KEY - Stability AI API key
"""

import os
import base64
import requests
from pathlib import Path
from typing import Optional


def generate_dalle(
    prompt: str,
    output_path: str = "dalle_output.png",
    model: str = "dall-e-3",
    size: str = "1024x1024",
    quality: str = "standard",
) -> str:
    """Generate an image using OpenAI's DALL-E."""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        response_format="b64_json",
        n=1,
    )

    image_data = base64.b64decode(response.data[0].b64_json)
    Path(output_path).write_bytes(image_data)
    return output_path


def generate_imagen(
    prompt: str,
    output_path: str = "imagen_output.png",
    model: str = "imagen-3.0-generate-002",
) -> str:
    """Generate an image using Google's Imagen."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    response = client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
        ),
    )

    if response.generated_images:
        image_data = response.generated_images[0].image.image_bytes
        Path(output_path).write_bytes(image_data)
        return output_path
    else:
        raise ValueError("No image generated")


def generate_stability(
    prompt: str,
    output_path: str = "stability_output.png",
    model: str = "stable-diffusion-xl-1024-v1-0",
    width: int = 1024,
    height: int = 1024,
) -> str:
    """Generate an image using Stability AI's API."""
    api_key = os.environ.get("STABILITY_API_KEY")

    response = requests.post(
        f"https://api.stability.ai/v1/generation/{model}/text-to-image",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={
            "text_prompts": [{"text": prompt, "weight": 1.0}],
            "cfg_scale": 7,
            "width": width,
            "height": height,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise ValueError(f"Stability API error: {response.text}")

    data = response.json()
    image_data = base64.b64decode(data["artifacts"][0]["base64"])
    Path(output_path).write_bytes(image_data)
    return output_path


def generate_all(prompt: str, output_dir: str = ".") -> dict[str, str]:
    """Generate images from all providers."""
    results = {}
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    try:
        results["dalle"] = generate_dalle(
            prompt, str(output_dir / "dalle_output.png")
        )
    except Exception as e:
        results["dalle"] = f"Error: {e}"

    try:
        results["imagen"] = generate_imagen(
            prompt, str(output_dir / "imagen_output.png")
        )
    except Exception as e:
        results["imagen"] = f"Error: {e}"

    try:
        results["stability"] = generate_stability(
            prompt, str(output_dir / "stability_output.png")
        )
    except Exception as e:
        results["stability"] = f"Error: {e}"

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate images using AI")
    parser.add_argument("prompt", help="The image description prompt")
    parser.add_argument(
        "--provider",
        choices=["dalle", "imagen", "stability", "all"],
        default="all",
        help="Which provider to use",
    )
    parser.add_argument(
        "--output", "-o",
        default="output.png",
        help="Output file path",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Output directory (for --provider all)",
    )
    args = parser.parse_args()

    if args.provider == "all":
        results = generate_all(args.prompt, args.output_dir)
        for provider, result in results.items():
            print(f"{provider}: {result}")
    else:
        func_map = {
            "dalle": generate_dalle,
            "imagen": generate_imagen,
            "stability": generate_stability,
        }
        output = func_map[args.provider](args.prompt, args.output)
        print(f"Image saved to: {output}")

#!/usr/bin/env python3
"""
Script to generate images using OpenAI, Google Imagen, and Stability AI (v2 - Latest Models January 2026).

Requirements:
    pip install openai google-genai requests

Environment variables:
    OPENAI_API_KEY - OpenAI API key
    GEMINI_API_KEY - Google AI API key
    STABILITY_API_KEY - Stability AI API key

Model Updates (v2):
    - OpenAI: dall-e-3 -> gpt-image-1.5 (released December 16, 2025)
    - Google: imagen-3.0-generate-002 -> imagen-4.0-generate-preview (released late 2025)
    - Stability AI: stable-diffusion-xl-1024-v1-0 -> sd3.5-large (Stable Diffusion 3.5 Large)
"""

import os
import base64
import requests
from pathlib import Path
from typing import Optional


def generate_openai_image(
    prompt: str,
    output_path: str = "openai_output.png",
    model: str = "gpt-image-1.5",
    size: str = "1024x1024",
    quality: str = "standard",
) -> str:
    """Generate an image using OpenAI's GPT Image model.

    Latest models (January 2026):
        - gpt-image-1.5: Flagship model, native multimodal approach
        - gpt-image-1: Previous generation
        - gpt-image-1-mini: Faster, lower cost
        - dall-e-3: Legacy (deprecated, end of support May 12, 2026)
    """
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
    model: str = "imagen-4.0-generate-preview",
) -> str:
    """Generate an image using Google's Imagen 4.

    Latest models (January 2026):
        - imagen-4.0-generate-preview: Standard model, up to 2K resolution
        - imagen-4.0-fast-generate-preview: Up to 10x faster
        - imagen-4.0-ultra-generate-preview: Maximum quality and photorealism
    """
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
    model: str = "sd3.5-large",
    width: int = 1024,
    height: int = 1024,
) -> str:
    """Generate an image using Stability AI's Stable Diffusion 3.5.

    Latest models (January 2026):
        - sd3.5-large: Most powerful, superior quality and prompt adherence
        - sd3.5-large-turbo: Faster, 4-step generation
        - sd3.5-medium: Balanced quality/customization, runs on consumer hardware
    """
    api_key = os.environ.get("STABILITY_API_KEY")

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "image/*",
        },
        files={"none": ""},
        data={
            "prompt": prompt,
            "model": model,
            "width": width,
            "height": height,
            "output_format": "png",
        },
    )

    if response.status_code != 200:
        raise ValueError(f"Stability API error: {response.text}")

    Path(output_path).write_bytes(response.content)
    return output_path


def generate_all(prompt: str, output_dir: str = ".") -> dict[str, str]:
    """Generate images from all providers."""
    results = {}
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    try:
        results["openai"] = generate_openai_image(
            prompt, str(output_dir / "openai_output.png")
        )
    except Exception as e:
        results["openai"] = f"Error: {e}"

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

    parser = argparse.ArgumentParser(
        description="Generate images using AI (v2 - Latest Models January 2026)"
    )
    parser.add_argument("prompt", help="The image description prompt")
    parser.add_argument(
        "--provider",
        choices=["openai", "imagen", "stability", "all"],
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
            "openai": generate_openai_image,
            "imagen": generate_imagen,
            "stability": generate_stability,
        }
        output = func_map[args.provider](args.prompt, args.output)
        print(f"Image saved to: {output}")

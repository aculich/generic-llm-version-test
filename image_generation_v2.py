#!/usr/bin/env python3
"""
Script to query image generation models from various providers.
V2 Version - Updated with latest model versions as of January 2026.

Supports: OpenAI DALL-E, Stability AI, Flux (via Replicate), and others.

Requires API keys to be set in environment variables:
- OPENAI_API_KEY (for DALL-E)
- STABILITY_API_KEY (for Stability AI)
- REPLICATE_API_TOKEN (for Replicate/Flux)

Latest Models Used (as of January 2026):
- OpenAI: dall-e-3 (Released: October 2023) - Still the latest DALL-E version
- Stability AI: stable-diffusion-3-medium-diffusers (Released: 2024) or flux models
- Replicate: black-forest-labs/flux-dev (Released: 2024) - Latest Flux model
"""

import os
import sys
from typing import Optional, Dict, Any
from pathlib import Path


def generate_image_openai(prompt: str, model: str = "dall-e-3", size: str = "1024x1024", 
                          quality: str = "standard", n: int = 1) -> Optional[Dict[str, Any]]:
    """
    Generate images using OpenAI DALL-E models.
    
    Args:
        prompt: The image generation prompt
        model: Model name ('dall-e-3' or 'dall-e-2')
        size: Image size ('1024x1024', '1792x1024', '1024x1792' for dall-e-3)
        quality: Image quality ('standard' or 'hd' for dall-e-3)
        n: Number of images (1 for dall-e-3, 1-10 for dall-e-2)
    
    Returns:
        Dictionary with image URLs and metadata, or None if error
    """
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY environment variable not set")
            return None
        
        client = OpenAI(api_key=api_key)
        
        if model == "dall-e-3":
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1  # dall-e-3 only supports n=1
            )
        else:  # dall-e-2
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                n=n
            )
        
        result = {
            "urls": [img.url for img in response.data],
            "model": model,
            "revised_prompt": getattr(response.data[0], 'revised_prompt', None)
        }
        
        return result
    
    except ImportError:
        print("Error: openai package not installed. Install with: pip install openai")
        return None
    except Exception as e:
        print(f"Error generating image with OpenAI: {e}")
        return None


def generate_image_stability(prompt: str, model: str = "stable-diffusion-3-medium-diffusers",
                             width: int = 1024, height: int = 1024, 
                             steps: int = 30) -> Optional[Dict[str, Any]]:
    """
    Generate images using Stability AI models.
    
    Args:
        prompt: The image generation prompt
        model: Model name (e.g., 'stable-diffusion-3-medium-diffusers', 
               'stable-diffusion-xl-1024-v1-0', 'stable-diffusion-v1-6')
        width: Image width in pixels
        height: Image height in pixels
        steps: Number of inference steps
    
    Returns:
        Dictionary with image data and metadata, or None if error
    """
    try:
        import base64
        import requests
        
        api_key = os.getenv("STABILITY_API_KEY")
        if not api_key:
            print("Error: STABILITY_API_KEY environment variable not set")
            return None
        
        api_host = os.getenv('API_HOST', 'https://api.stability.ai')
        url = f"{api_host}/v1/generation/{model}/text-to-image"
        
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "text_prompts[0][text]": prompt,
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": steps,
        }
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code != 200:
            print(f"Error: API request failed with status {response.status_code}")
            print(response.text)
            return None
        
        result = response.json()
        
        # Save image to file
        output_dir = Path("generated_images")
        output_dir.mkdir(exist_ok=True)
        
        image_paths = []
        for i, image in enumerate(result.get("artifacts", [])):
            image_data = base64.b64decode(image["base64"])
            image_path = output_dir / f"stability_{model.replace('/', '_')}_{i}.png"
            with open(image_path, "wb") as f:
                f.write(image_data)
            image_paths.append(str(image_path))
        
        return {
            "image_paths": image_paths,
            "model": model,
            "seed": result.get("artifacts", [{}])[0].get("seed")
        }
    
    except ImportError:
        print("Error: requests package not installed. Install with: pip install requests")
        return None
    except Exception as e:
        print(f"Error generating image with Stability AI: {e}")
        return None


def generate_image_replicate(prompt: str, model: str = "black-forest-labs/flux-dev") -> Optional[Dict[str, Any]]:
    """
    Generate images using Replicate (supports various models including Flux).
    
    Args:
        prompt: The image generation prompt
        model: Model identifier (e.g., 'black-forest-labs/flux-dev', 
               'black-forest-labs/flux-schnell', 'stability-ai/sdxl:...', etc.)
    
    Returns:
        Dictionary with image URLs and metadata, or None if error
    """
    try:
        import replicate
        
        api_token = os.getenv("REPLICATE_API_TOKEN")
        if not api_token:
            print("Error: REPLICATE_API_TOKEN environment variable not set")
            return None
        
        os.environ["REPLICATE_API_TOKEN"] = api_token
        
        # Flux models may have different input parameters
        if "flux" in model.lower():
            output = replicate.run(
                model,
                input={
                    "prompt": prompt,
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "output_format": "png"
                }
            )
        else:
            # For other models (SDXL, etc.)
            output = replicate.run(
                model,
                input={"prompt": prompt}
            )
        
        # Replicate returns different formats depending on the model
        if isinstance(output, list):
            urls = output
        elif isinstance(output, str):
            urls = [output]
        else:
            urls = [str(output)]
        
        return {
            "urls": urls,
            "model": model
        }
    
    except ImportError:
        print("Error: replicate package not installed. Install with: pip install replicate")
        return None
    except Exception as e:
        print(f"Error generating image with Replicate: {e}")
        return None


def download_image(url: str, output_path: str) -> bool:
    """Download an image from a URL to a local file."""
    try:
        import requests
        
        response = requests.get(url)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False


def main():
    """Main function to demonstrate usage."""
    if len(sys.argv) < 2:
        print("Usage: python image_generation_v2.py '<prompt>' [provider] [options]")
        print("\nProviders:")
        print("  openai    - OpenAI DALL-E models (dall-e-3)")
        print("  stability - Stability AI models (stable-diffusion-3, SDXL)")
        print("  replicate - Replicate (Flux, SDXL, and other models)")
        print("\nExamples:")
        print("  python image_generation_v2.py 'a futuristic city' openai")
        print("  python image_generation_v2.py 'a beautiful landscape' stability")
        print("  python image_generation_v2.py 'an abstract painting' replicate")
        sys.exit(1)
    
    prompt = sys.argv[1]
    provider = sys.argv[2].lower() if len(sys.argv) > 2 else "openai"
    
    print(f"Generating image with {provider} (using latest models)...")
    print(f"Prompt: {prompt}\n")
    
    if provider == "openai":
        result = generate_image_openai(prompt)
        if result:
            print("Generated image URLs:")
            for i, url in enumerate(result["urls"]):
                print(f"  {i+1}. {url}")
                # Download the image
                output_dir = Path("generated_images")
                output_dir.mkdir(exist_ok=True)
                output_path = output_dir / f"dalle_{i}.png"
                if download_image(url, str(output_path)):
                    print(f"     Downloaded to: {output_path}")
            if result.get("revised_prompt"):
                print(f"\nRevised prompt: {result['revised_prompt']}")
    
    elif provider == "stability":
        result = generate_image_stability(prompt)
        if result:
            print("Generated images saved to:")
            for path in result["image_paths"]:
                print(f"  - {path}")
            if result.get("seed"):
                print(f"\nSeed: {result['seed']}")
    
    elif provider == "replicate":
        result = generate_image_replicate(prompt)
        if result:
            print("Generated image URLs:")
            for i, url in enumerate(result["urls"]):
                print(f"  {i+1}. {url}")
                # Download the image
                output_dir = Path("generated_images")
                output_dir.mkdir(exist_ok=True)
                output_path = output_dir / f"replicate_{i}.png"
                if download_image(url, str(output_path)):
                    print(f"     Downloaded to: {output_path}")
    
    else:
        print(f"Unknown provider: {provider}")
        print("Available providers: openai, stability, replicate")
        sys.exit(1)


if __name__ == "__main__":
    main()


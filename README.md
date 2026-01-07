# LLM and Image Generation Scripts

This repository contains Python scripts to query various LLM providers and image generation models.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up API keys as environment variables:
```bash
# For text generation
export GOOGLE_API_KEY="your-google-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# For image generation
export STABILITY_API_KEY="your-stability-api-key"  # Optional
export REPLICATE_API_TOKEN="your-replicate-token"  # Optional
```

## Usage

### Text Generation (`query_llms.py`)

Query text generation models from Gemini, OpenAI, and Anthropic.

**Basic usage:**
```bash
# Query all providers
python query_llms.py "What is artificial intelligence?"

# Query specific provider
python query_llms.py "What is AI?" gemini

# Query specific provider and model
python query_llms.py "What is AI?" openai gpt-4o
python query_llms.py "What is AI?" anthropic claude-3-5-sonnet-20241022
```

**Available models:**

- **Gemini**: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-pro`
- **OpenAI**: `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`, `o1-preview`, `o1-mini`
- **Anthropic**: `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022`, `claude-3-opus-20240229`

### Image Generation (`image_generation.py`)

Generate images using various providers.

**Basic usage:**
```bash
# OpenAI DALL-E (default)
python image_generation.py "a futuristic cityscape at sunset"

# Stability AI
python image_generation.py "a beautiful mountain landscape" stability

# Replicate (various models)
python image_generation.py "an abstract digital art piece" replicate
```

**Providers:**
- **OpenAI**: DALL-E 2 and DALL-E 3
- **Stability AI**: Stable Diffusion models
- **Replicate**: Various models including Midjourney-style generators

Generated images are saved to the `generated_images/` directory.

## Scripts

### Original Versions
- `query_llms.py` - Query text generation models (original version)
- `image_generation.py` - Generate images from various providers (original version)

### V2 Versions (Latest Models - January 2026)
- `query_llms_v2.py` - Query text generation models with latest model versions
- `image_generation_v2.py` - Generate images with latest model versions

### Documentation
- `requirements.txt` - Python dependencies
- `MODEL_VERSION_COMPARISON.md` - Detailed comparison of original vs v2 model versions

## V2 Scripts - Latest Models

The v2 scripts use the latest available models as of January 2026:

### Text Generation (query_llms_v2.py)

**Latest Models:**
- **Gemini**: `gemini-2.0-flash-exp` (Released: February 5, 2025)
- **OpenAI**: `gpt-4o-2025-01-07` (Released: January 7, 2025)
- **Anthropic**: `claude-3-7-sonnet-20250224` (Released: February 24, 2025)

**Usage:**
```bash
# Query all providers with latest models
python query_llms_v2.py "What is artificial intelligence?"

# Query specific provider
python query_llms_v2.py "What is AI?" gemini

# Query specific provider and model
python query_llms_v2.py "What is AI?" openai gpt-4o-2025-01-07
python query_llms_v2.py "What is AI?" anthropic claude-3-7-sonnet-20250224
```

### Image Generation (image_generation_v2.py)

**Latest Models:**
- **OpenAI**: `dall-e-3` (Still latest as of January 2026)
- **Stability AI**: `stable-diffusion-3-medium-diffusers` (Released: 2024)
- **Replicate**: `black-forest-labs/flux-dev` (Released: 2024) - State-of-the-art quality

**Usage:**
```bash
# OpenAI DALL-E 3 (default)
python image_generation_v2.py "a futuristic cityscape at sunset"

# Stability AI (Stable Diffusion 3)
python image_generation_v2.py "a beautiful mountain landscape" stability

# Replicate (Flux - latest)
python image_generation_v2.py "an abstract digital art piece" replicate
```

For detailed information about model versions and release dates, see `MODEL_VERSION_COMPARISON.md`.


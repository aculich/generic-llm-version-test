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

- `query_llms.py` - Query text generation models
- `image_generation.py` - Generate images from various providers
- `requirements.txt` - Python dependencies


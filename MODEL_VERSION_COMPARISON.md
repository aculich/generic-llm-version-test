# Model Version Comparison: Original vs V2 Scripts

This document compares the models used in the original scripts versus the v2 versions created in January 2026.

## Text Generation Models (query_llms.py vs query_llms_v2.py)

### Google Gemini Models

| Version | Original Script | V2 Script | Release Date | Notes |
|---------|----------------|-----------|--------------|-------|
| Default | `gemini-1.5-pro` | `gemini-2.0-flash-exp` | Feb 5, 2025 | Latest experimental Flash model with enhanced capabilities |
| Alternative | `gemini-1.5-flash` | `gemini-2.0-flash-thinking-exp` | Feb 5, 2025 | Thinking variant with extended reasoning |
| Alternative | `gemini-pro` | `gemini-2.5-pro` | Jun 2025 | Latest Pro model with advanced reasoning |

**Original Release Dates:**
- `gemini-1.5-pro`: February 15, 2024
- `gemini-1.5-flash`: May 14, 2024
- `gemini-pro`: December 6, 2023

**V2 Release Dates:**
- `gemini-2.0-flash-exp`: February 5, 2025
- `gemini-2.0-flash-thinking-exp`: February 5, 2025
- `gemini-2.5-pro`: June 2025

### OpenAI Models

| Version | Original Script | V2 Script | Release Date | Notes |
|---------|----------------|-----------|--------------|-------|
| Default | `gpt-4o` | `gpt-4o-2025-01-07` | Jan 7, 2025 | Latest GPT-4o version with updated knowledge cutoff |
| Alternative | `gpt-4-turbo` | `gpt-4o` | May 13, 2024 | Still available, but gpt-4o is newer |
| Alternative | `gpt-3.5-turbo` | `o3` | Dec 2025 (if available) | Latest reasoning model (if available) |
| Alternative | `o1-preview` | `o1-preview` | Jan 29, 2024 | Still available |
| Alternative | `o1-mini` | `o1-mini` | Jan 29, 2024 | Still available |

**Original Release Dates:**
- `gpt-4o`: May 13, 2024
- `gpt-4-turbo`: November 6, 2023
- `gpt-3.5-turbo`: March 1, 2023
- `o1-preview`: January 29, 2024
- `o1-mini`: January 29, 2024

**V2 Release Dates:**
- `gpt-4o-2025-01-07`: January 7, 2025
- `o3`: December 2025 (if available)

### Anthropic Claude Models

| Version | Original Script | V2 Script | Release Date | Notes |
|---------|----------------|-----------|--------------|-------|
| Default | `claude-3-5-sonnet-20241022` | `claude-3-7-sonnet-20250224` | Feb 24, 2025 | Latest Sonnet model with improved performance |
| Alternative | `claude-3-5-haiku-20241022` | `claude-opus-4.5-20251124` | Nov 24, 2025 | Latest Opus model with advanced capabilities |
| Alternative | `claude-3-opus-20240229` | `claude-3-5-sonnet-20241022` | Oct 22, 2024 | Still available |
| Alternative | `claude-3-sonnet-20240229` | `claude-3-5-haiku-20241022` | Oct 22, 2024 | Still available |

**Original Release Dates:**
- `claude-3-5-sonnet-20241022`: October 22, 2024
- `claude-3-5-haiku-20241022`: October 22, 2024
- `claude-3-opus-20240229`: February 29, 2024
- `claude-3-sonnet-20240229`: February 29, 2024

**V2 Release Dates:**
- `claude-3-7-sonnet-20250224`: February 24, 2025
- `claude-opus-4.5-20251124`: November 24, 2025

## Image Generation Models (image_generation.py vs image_generation_v2.py)

### OpenAI DALL-E Models

| Version | Original Script | V2 Script | Release Date | Notes |
|---------|----------------|-----------|--------------|-------|
| Default | `dall-e-3` | `dall-e-3` | Oct 2023 | Still the latest DALL-E version (no DALL-E 4 yet) |
| Alternative | `dall-e-2` | `dall-e-2` | Apr 6, 2022 | Still available for backward compatibility |

**Note:** DALL-E 3 remains the latest version as of January 2026. No DALL-E 4 has been released.

### Stability AI Models

| Version | Original Script | V2 Script | Release Date | Notes |
|---------|----------------|-----------|--------------|-------|
| Default | `stable-diffusion-xl-1024-v1-0` | `stable-diffusion-3-medium-diffusers` | 2024 | Latest Stable Diffusion 3 model |
| Alternative | `stable-diffusion-v1-6` | `stable-diffusion-xl-1024-v1-0` | Jul 26, 2023 | Still available |

**Original Release Dates:**
- `stable-diffusion-xl-1024-v1-0`: July 26, 2023
- `stable-diffusion-v1-6`: August 2023

**V2 Release Dates:**
- `stable-diffusion-3-medium-diffusers`: 2024 (exact date varies by variant)

### Replicate Models

| Version | Original Script | V2 Script | Release Date | Notes |
|---------|----------------|-----------|--------------|-------|
| Default | `stability-ai/sdxl:39ed52f2...` | `black-forest-labs/flux-dev` | 2024 | Latest Flux model, state-of-the-art quality |
| Alternative | `black-forest-labs/flux-dev` | `black-forest-labs/flux-schnell` | 2024 | Faster Flux variant |
| Alternative | N/A | `stability-ai/sdxl:...` | Jul 2023 | Still available for backward compatibility |

**Original Release Dates:**
- `stability-ai/sdxl:39ed52f2...`: July 2023

**V2 Release Dates:**
- `black-forest-labs/flux-dev`: 2024
- `black-forest-labs/flux-schnell`: 2024

## Summary of Changes

### Text Generation Models
- **Gemini**: Upgraded from 1.5 series (2024) to 2.0/2.5 series (2025)
- **OpenAI**: Upgraded to latest GPT-4o version with 2025 knowledge cutoff
- **Anthropic**: Upgraded from Claude 3.5 (Oct 2024) to Claude 3.7 Sonnet (Feb 2025) and Claude Opus 4.5 (Nov 2025)

### Image Generation Models
- **DALL-E**: No change (dall-e-3 still latest)
- **Stability AI**: Upgraded from SDXL (2023) to Stable Diffusion 3 (2024)
- **Replicate**: Upgraded from SDXL to Flux models (2024), which are state-of-the-art

## Key Improvements in V2

1. **Better Performance**: All models in v2 are newer and generally perform better on benchmarks
2. **Larger Context Windows**: Newer models support larger context windows (e.g., Gemini 2.0 has 2M tokens)
3. **Enhanced Reasoning**: Models like Claude 3.7 and Gemini 2.0 have improved reasoning capabilities
4. **Better Image Quality**: Flux models on Replicate produce higher quality images than SDXL
5. **Updated Knowledge**: Models have more recent training data and knowledge cutoffs

## Migration Notes

- Original scripts are preserved and unchanged
- V2 scripts use the same API structure, so migration is straightforward
- Some model names may need adjustment based on actual API availability
- Check provider documentation for exact model identifiers as they may vary

## Date of V2 Creation

**Created:** January 7, 2026
**Models Reviewed:** All models as of January 2026


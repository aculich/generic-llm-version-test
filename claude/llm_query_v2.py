#!/usr/bin/env python3
"""
Script to query Gemini, OpenAI, and Anthropic models (v2 - Latest Models January 2026).

Requirements:
    pip install google-genai openai anthropic

Environment variables:
    GEMINI_API_KEY - Google AI API key
    OPENAI_API_KEY - OpenAI API key
    ANTHROPIC_API_KEY - Anthropic API key

Model Updates (v2):
    - OpenAI: gpt-4o -> gpt-5.2 (released December 11, 2025)
    - Google: gemini-2.0-flash -> gemini-3-flash-preview (released late 2025)
    - Anthropic: claude-sonnet-4-20250514 -> claude-opus-4-5-20251101 (released November 2025)
"""

import os
from typing import Optional


def query_gemini(prompt: str, model: str = "gemini-3-flash-preview") -> str:
    """Query Google's Gemini model.

    Latest models (January 2026):
        - gemini-3-flash-preview: Fast frontier-class performance
        - gemini-3-pro: Best for advanced math and coding
        - gemini-2.5-pro: Previous generation flagship
    """
    from google import genai

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    return response.text


def query_openai(
    prompt: str,
    model: str = "gpt-5.2",
    system_prompt: Optional[str] = None,
) -> str:
    """Query OpenAI's models.

    Latest models (January 2026):
        - gpt-5.2: Most capable model, 400K context, 128K output tokens
        - gpt-5.2-codex: Optimized for agentic coding
        - o3: Most powerful reasoning model
        - o3-mini: Cost-efficient reasoning (low/medium/high effort)
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content


def query_anthropic(
    prompt: str,
    model: str = "claude-opus-4-5-20251101",
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
) -> str:
    """Query Anthropic's Claude models.

    Latest models (January 2026):
        - claude-opus-4-5-20251101: Most intelligent, best for coding/agents
        - claude-opus-4-1-20250805: Previous flagship with strong agentic performance
        - claude-sonnet-4-20250514: Balanced performance and cost
    """
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    response = client.messages.create(**kwargs)
    return response.content[0].text


def query_all(prompt: str) -> dict[str, str]:
    """Query all three providers with the same prompt."""
    results = {}

    try:
        results["gemini"] = query_gemini(prompt)
    except Exception as e:
        results["gemini"] = f"Error: {e}"

    try:
        results["openai"] = query_openai(prompt)
    except Exception as e:
        results["openai"] = f"Error: {e}"

    try:
        results["anthropic"] = query_anthropic(prompt)
    except Exception as e:
        results["anthropic"] = f"Error: {e}"

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Query LLM APIs (v2 - Latest Models January 2026)"
    )
    parser.add_argument("prompt", help="The prompt to send")
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai", "anthropic", "all"],
        default="all",
        help="Which provider to query",
    )
    parser.add_argument("--model", help="Specific model to use")
    args = parser.parse_args()

    if args.provider == "all":
        results = query_all(args.prompt)
        for provider, response in results.items():
            print(f"\n{'='*50}")
            print(f"{provider.upper()}:")
            print(f"{'='*50}")
            print(response)
    else:
        func_map = {
            "gemini": query_gemini,
            "openai": query_openai,
            "anthropic": query_anthropic,
        }
        func = func_map[args.provider]
        kwargs = {"prompt": args.prompt}
        if args.model:
            kwargs["model"] = args.model
        print(func(**kwargs))

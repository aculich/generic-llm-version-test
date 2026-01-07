#!/usr/bin/env python3
"""
Script to query text generation models from Gemini, OpenAI, and Anthropic.
Requires API keys to be set in environment variables:
- GOOGLE_API_KEY (for Gemini)
- OPENAI_API_KEY (for OpenAI)
- ANTHROPIC_API_KEY (for Anthropic)
"""

import os
import sys
from typing import Optional, Dict, Any


def query_gemini(prompt: str, model: str = "gemini-1.5-pro") -> Optional[str]:
    """
    Query Google Gemini models.
    
    Args:
        prompt: The input prompt
        model: Model name (e.g., 'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro')
    
    Returns:
        Response text or None if error
    """
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable not set")
            return None
        
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(model)
        
        response = model_instance.generate_content(prompt)
        return response.text
    
    except ImportError:
        print("Error: google-generativeai package not installed. Install with: pip install google-generativeai")
        return None
    except Exception as e:
        print(f"Error querying Gemini: {e}")
        return None


def query_openai(prompt: str, model: str = "gpt-4o") -> Optional[str]:
    """
    Query OpenAI models.
    
    Args:
        prompt: The input prompt
        model: Model name (e.g., 'gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo', 'o1-preview', 'o1-mini')
    
    Returns:
        Response text or None if error
    """
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY environment variable not set")
            return None
        
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    
    except ImportError:
        print("Error: openai package not installed. Install with: pip install openai")
        return None
    except Exception as e:
        print(f"Error querying OpenAI: {e}")
        return None


def query_anthropic(prompt: str, model: str = "claude-3-5-sonnet-20241022") -> Optional[str]:
    """
    Query Anthropic Claude models.
    
    Args:
        prompt: The input prompt
        model: Model name (e.g., 'claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022', 
               'claude-3-opus-20240229', 'claude-3-sonnet-20240229')
    
    Returns:
        Response text or None if error
    """
    try:
        from anthropic import Anthropic
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: ANTHROPIC_API_KEY environment variable not set")
            return None
        
        client = Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    except ImportError:
        print("Error: anthropic package not installed. Install with: pip install anthropic")
        return None
    except Exception as e:
        print(f"Error querying Anthropic: {e}")
        return None


def main():
    """Main function to demonstrate usage."""
    if len(sys.argv) < 2:
        print("Usage: python query_llms.py '<prompt>' [provider] [model]")
        print("\nProviders: gemini, openai, anthropic")
        print("\nExample models:")
        print("  Gemini: gemini-1.5-pro, gemini-1.5-flash, gemini-pro")
        print("  OpenAI: gpt-4o, gpt-4-turbo, gpt-3.5-turbo, o1-preview, o1-mini")
        print("  Anthropic: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022")
        print("\nExample:")
        print("  python query_llms.py 'What is AI?' gemini gemini-1.5-pro")
        sys.exit(1)
    
    prompt = sys.argv[1]
    provider = sys.argv[2].lower() if len(sys.argv) > 2 else None
    model = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Default models if not specified
    default_models = {
        "gemini": "gemini-1.5-pro",
        "openai": "gpt-4o",
        "anthropic": "claude-3-5-sonnet-20241022"
    }
    
    if provider:
        if provider == "gemini":
            model = model or default_models["gemini"]
            print(f"Querying Gemini ({model})...")
            response = query_gemini(prompt, model)
        elif provider == "openai":
            model = model or default_models["openai"]
            print(f"Querying OpenAI ({model})...")
            response = query_openai(prompt, model)
        elif provider == "anthropic":
            model = model or default_models["anthropic"]
            print(f"Querying Anthropic ({model})...")
            response = query_anthropic(prompt, model)
        else:
            print(f"Unknown provider: {provider}")
            sys.exit(1)
        
        if response:
            print("\nResponse:")
            print(response)
        else:
            sys.exit(1)
    else:
        # Query all providers
        print("Querying all providers...\n")
        
        print("=" * 60)
        print("GEMINI")
        print("=" * 60)
        response = query_gemini(prompt, default_models["gemini"])
        if response:
            print(response)
        print()
        
        print("=" * 60)
        print("OPENAI")
        print("=" * 60)
        response = query_openai(prompt, default_models["openai"])
        if response:
            print(response)
        print()
        
        print("=" * 60)
        print("ANTHROPIC")
        print("=" * 60)
        response = query_anthropic(prompt, default_models["anthropic"])
        if response:
            print(response)


if __name__ == "__main__":
    main()


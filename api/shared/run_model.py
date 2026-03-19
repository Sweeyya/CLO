import os
import subprocess
import logging

# Which provider backend to use
# Options: "ollama" (local dev), "anthropic", "openai", "azure_openai"
# Each provider will have its own adapter function
PROVIDER = os.getenv("CLO_PROVIDER", "ollama")

# Build allowed models from the configured tiers
from api.shared.decision import MODEL_SMALL, MODEL_MID, MODEL_LARGE
ALLOWED_MODELS = {MODEL_SMALL, MODEL_MID, MODEL_LARGE}


def run_model(prompt: str, model: str) -> str:
    """
    Route inference to the configured provider.
    Same interface regardless of backend — give it a prompt and model, get text back.
    """
    if model not in ALLOWED_MODELS:
        logging.warning(f"Blocked attempt to run unrecognized model: {model}")
        return ""

    if PROVIDER == "ollama":
        return _run_ollama(prompt, model)
    elif PROVIDER == "anthropic":
        return _run_anthropic(prompt, model)
    # elif PROVIDER == "openai":
    #     return _run_openai(prompt, model)
    else:
        logging.error(f"Unknown provider: {PROVIDER}")
        return ""


def _run_ollama(prompt: str, model: str) -> str:
    """
    Local development adapter — runs models through Ollama CLI.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            logging.error(f"Ollama returned error for model {model}: {result.stderr}")
            return ""
    except subprocess.TimeoutExpired:
        logging.error(f"Ollama timed out after 60s for model {model}")
        return ""
    except Exception as e:
        logging.error(f"Failed to run Ollama: {e}", exc_info=True)
        return ""


# --- Future provider adapters ---
# Each one follows the same pattern: (prompt, model) -> str


def _run_anthropic(prompt: str, model: str) -> str:
    """Adapter for Anthropic API (Claude Haiku/Sonnet/Opus)."""
    import anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    try:
        client = anthropic.Anthropic(api_key=api_key, timeout=60.0)
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        if not response.content:
            logging.error(f"Anthropic returned empty content for model {model}")
            return ""
        return response.content[0].text
    except anthropic.AuthenticationError:
        logging.error("Anthropic authentication failed — check ANTHROPIC_API_KEY")
        return ""
    except anthropic.RateLimitError:
        logging.error(f"Anthropic rate limit exceeded for model {model}")
        return ""
    except Exception as e:
        logging.error(f"Anthropic request failed for model {model}: {type(e).__name__}", exc_info=True)
        return ""


# def _run_openai(prompt: str, model: str) -> str:
#     """Adapter for OpenAI API (GPT-4o / GPT-4o-mini)"""
#     from openai import OpenAI
#     client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#     response = client.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content
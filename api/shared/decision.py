# api/shared/decision.py
import os

# --- Provider Configuration ---
# Each AI company sets these to their own model names.
# Examples:
#   Anthropic:  small=haiku, mid=sonnet, large=opus
#   OpenAI:     small=gpt-4o-mini, mid=gpt-4o, large=o1
#   Google:     small=gemini-flash, mid=gemini-pro, large=gemini-ultra
#   Dev/local:  small=phi3:mini, mid=mistral, large=phi3:large
MODEL_SMALL = os.getenv("CLO_MODEL_SMALL", "phi3:mini")
MODEL_MID = os.getenv("CLO_MODEL_MID", "mistral")
MODEL_LARGE = os.getenv("CLO_MODEL_LARGE", "phi3:large")

# Carbon intensity threshold — below this is "clean grid"
# Uses env var from config, falls back to 0.4
CLEAN_GRID_THRESHOLD = float(os.getenv("CARBON_GREEN_THRESHOLD_KG", "0.4"))


def choose_model(prompt_complexity: str, region_intensity: float) -> str:
    """
    Pick the most carbon-efficient model that can still handle the prompt.

    Rules:
    - Complexity sets a quality floor (high → at least mid-tier)
    - Grid intensity can downgrade within the allowed range, never below the floor
    - Model names come from environment config — works with any provider
    """
    if prompt_complexity == "high":
        if region_intensity <= CLEAN_GRID_THRESHOLD:
            return MODEL_LARGE
        return MODEL_MID

    if prompt_complexity == "medium":
        if region_intensity <= CLEAN_GRID_THRESHOLD:
            return MODEL_MID
        return MODEL_SMALL

    # Low complexity — always use the smallest model
    return MODEL_SMALL

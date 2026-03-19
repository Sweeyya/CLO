# api/shared/decision.py

def choose_model(prompt_complexity: str, region_intensity: float) -> str:
    """
    Simple decision logic to pick the most efficient model based on prompt complexity
    and local grid carbon intensity.
    """
    # If the grid is dirty (high carbon) or prompt is simple → use smaller model
    if prompt_complexity == "low" or region_intensity > 0.4:
        return "phi3:mini"

    # Medium complexity → slightly larger model
    if prompt_complexity == "medium":
        return "mistral"

    # High complexity or clean region → biggest model
    return "gpt4"

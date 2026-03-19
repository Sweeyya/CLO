import time
import json
import logging
import azure.functions as func

from api.shared.energy import track_inference_energy
from api.shared.carbon import calculate_carbon, get_regional_intensity_if_available
from api.shared.run_model import run_model
from api.shared.decision import choose_model

MAX_PROMPT_LENGTH = 10000  # character cap to prevent abuse

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('CLO inference request received.')

    try:
        body = req.get_json()
        prompt = body.get("prompt", "")

        # --- Input validation ---
        if not prompt or not prompt.strip():
            return func.HttpResponse(
                json.dumps({"ok": False, "error": "Prompt is required."}),
                status_code=400,
                mimetype="application/json"
            )

        if len(prompt) > MAX_PROMPT_LENGTH:
            return func.HttpResponse(
                json.dumps({"ok": False, "error": f"Prompt exceeds max length of {MAX_PROMPT_LENGTH} characters."}),
                status_code=400,
                mimetype="application/json"
            )

        # --- CLO decides region and model (not the user) ---
        # TODO: Replace with live grid intensity lookup per region
        region, intensity = _pick_cleanest_region()

        # TODO: Replace with real prompt complexity analysis
        prompt_complexity = "low"  # placeholder
        model = choose_model(prompt_complexity, intensity)

        # --- Run inference and measure ---
        start = time.time()
        output, energy_kwh = track_inference_energy(lambda: run_model(prompt, model), model)
        duration = time.time() - start

        if not output:
            logging.error(f"Model {model} returned empty output for prompt.")
            return func.HttpResponse(
                json.dumps({"ok": False, "error": "Model failed to generate a response."}),
                status_code=502,
                mimetype="application/json"
            )
        carbon_kg = calculate_carbon(energy_kwh, region=region)

        result = {
            "ok": True,
            "model": model,
            "duration_sec": round(duration, 2),
            "energy_kwh": energy_kwh,
            "carbon_kg": carbon_kg,
            "region": region,
            "output": output
        }

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "Invalid request body. Expected JSON."}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"CLO inference failed: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"ok": False, "error": "Internal server error."}),
            status_code=500,
            mimetype="application/json"
        )


def _pick_cleanest_region() -> tuple[str, float]:
    """
    Pick the region with the lowest carbon intensity right now.
    Returns (region_name, intensity_value).
    TODO: Replace with live API calls to WattTime or ElectricityMaps.
    """
    regions = ["us-east", "us-west", "eu-central", "norway", "india", "china"]
    scored = [(r, get_regional_intensity_if_available(r)) for r in regions]
    best_region, best_intensity = min(scored, key=lambda x: x[1])
    return best_region, best_intensity
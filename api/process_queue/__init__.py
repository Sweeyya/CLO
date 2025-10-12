import json
import time
import logging
import azure.functions as func

from api.shared.energy import measure_energy_usage
from api.shared.carbon import calculate_carbon

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("CLO /infer invoked")

    try:
        _ = req.get_json()
    except Exception:
        pass

    start = time.time()
    time.sleep(1.2)  # simulate inference
    duration = time.time() - start

    model_name = "phi3:mini"
    region = "us-east"
    energy_kwh = measure_energy_usage(model_name, duration)
    carbon_kg = calculate_carbon(energy_kwh, region=region)

    result = {
        "model": model_name,
        "duration_sec": round(duration, 2),
        "energy_kwh": energy_kwh,
        "carbon_kg": carbon_kg,
        "region": region
    }

    return func.HttpResponse(
        json.dumps(result),
        status_code=200,
        mimetype="application/json"
    )

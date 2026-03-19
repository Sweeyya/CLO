import time
import json
import logging
import azure.functions as func

from api.shared.energy import measure_energy_usage
from api.shared.carbon import calculate_carbon
from api.shared.run_model import run_local_model

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('CLO inference request received.')

    try:
        body = req.get_json()
        prompt = body.get("prompt", "")
        region = body.get("region", "us-east")
        model = body.get("model", "phi3:mini")

        # Run model and measure time
        start = time.time()
        output = run_local_model(prompt, model)
        end = time.time()

        duration = end - start
        energy_kwh = measure_energy_usage(model, duration)
        carbon_kg = calculate_carbon(energy_kwh)

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
            body=json.dumps(result, indent=2),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        error = {"ok": False, "error": str(e)}
        return func.HttpResponse(json.dumps(error), status_code=500)

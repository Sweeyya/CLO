import json
import time
import logging
import azure.functions as func

# Try imports inside the handler so we can show import errors in the response
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info("CLO /infer invoked (debug mode)")

        # Attempt imports (common failure point)
        try:
            from api.shared.energy import measure_energy_usage
            from api.shared.carbon import calculate_carbon
        except Exception as e:
            return func.HttpResponse(
                json.dumps({"ok": False, "where": "imports", "error": str(e)}),
                status_code=500, mimetype="application/json"
            )

        # Ignore body, just run the demo
        start = time.time()
        time.sleep(1.0)
        duration = time.time() - start

        model_name = "phi3:mini"
        region = "us-east"
        energy_kwh = measure_energy_usage(model_name, duration)
        carbon_kg = calculate_carbon(energy_kwh, region=region)

        result = {
            "ok": True,
            "model": model_name,
            "duration_sec": round(duration, 2),
            "energy_kwh": energy_kwh,
            "carbon_kg": carbon_kg,
            "region": region
        }
        return func.HttpResponse(json.dumps(result), status_code=200, mimetype="application/json")

    except Exception as e:
        # Catch any other runtime errors and show them
        return func.HttpResponse(
            json.dumps({"ok": False, "where": "runtime", "error": str(e)}),
            status_code=500, mimetype="application/json"
        )

import logging
import os
import time

from api.shared.decision import MODEL_SMALL, MODEL_MID, MODEL_LARGE

try:
    from codecarbon import OfflineEmissionsTracker
    _HAS_CODECARBON = True
except ImportError:
    _HAS_CODECARBON = False

# Estimated power draw (Watts) per model tier
# These are rough estimates — in production, replace with real telemetry
# Provider can override via env vars
WATTS_SMALL = int(os.getenv("CLO_WATTS_SMALL", "50"))
WATTS_MID = int(os.getenv("CLO_WATTS_MID", "150"))
WATTS_LARGE = int(os.getenv("CLO_WATTS_LARGE", "300"))

# Map configured model names to their wattage
MODEL_POWER = {
    MODEL_SMALL: WATTS_SMALL,
    MODEL_MID: WATTS_MID,
    MODEL_LARGE: WATTS_LARGE,
}

DEFAULT_WATTS = 100


def measure_energy_usage(model_name: str, duration_seconds: float) -> float:
    """
    Estimate energy consumption (kWh) based on model tier and duration.
    Formula: watts × hours / 1000 = kWh
    """
    watts = MODEL_POWER.get(model_name, DEFAULT_WATTS)
    hours = duration_seconds / 3600.0
    kwh = watts * hours / 1000.0
    return round(kwh, 6)


def track_inference_energy(inference_fn, model_name: str):
    """
    Run inference_fn() and measure actual energy consumption (kWh).

    Uses CodeCarbon's OfflineEmissionsTracker when available.
    Falls back to the wattage-based estimate if CodeCarbon is not installed or fails.

    Returns:
        (result, kwh): the return value of inference_fn() and energy in kWh.
    """
    if _HAS_CODECARBON:
        try:
            country_code = os.getenv("CLO_COUNTRY_ISO_CODE", "USA")
            tracker = OfflineEmissionsTracker(
                country_iso_code=country_code,
                save_to_file=False,
                log_level="error",
            )
            tracker.start()
            start = time.time()
            result = inference_fn()
            duration = time.time() - start
            tracker.stop()
            data = tracker.final_emissions_data
            kwh = round(data.energy_consumed, 6) if data else measure_energy_usage(model_name, duration)
            return result, kwh
        except Exception as e:
            logging.warning(
                f"CodeCarbon measurement failed for model {model_name} ({type(e).__name__}), "
                "falling back to estimate"
            )

    start = time.time()
    result = inference_fn()
    duration = time.time() - start
    return result, measure_energy_usage(model_name, duration)
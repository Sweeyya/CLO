def measure_energy_usage(model_name: str, duration_seconds: float) -> float:
    """
    Simulate measuring energy consumption (kWh) based on how long a model runs.
    Later, this can be replaced with real telemetry.
    """
    # Approx energy draw (Watts) by model type — just placeholder constants for now
    model_power = {
        "phi3:mini": 50,     # light model ~50W
        "phi3:medium": 120,  # medium model ~120W
        "phi3:large": 250,   # large model ~250W
    }

    watts = model_power.get(model_name, 100)
    hours = duration_seconds / 3600.0
    kwh = watts * hours / 1000.0
    return round(kwh, 6)

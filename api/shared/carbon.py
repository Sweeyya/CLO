def calculate_carbon(energy_kwh: float, region: str = "us-east") -> float:
    """
    Convert energy use (kWh) into carbon emissions (kg CO2e)
    using an estimated carbon intensity for the region.
    """
    grid_intensity = {
        "us-east": 0.35,   # 0.35 kg CO2 per kWh (avg)
        "us-west": 0.25,
        "eu-central": 0.15,
        "asia-east": 0.55
    }

    kg_co2 = energy_kwh * grid_intensity.get(region, 0.35)
    return round(kg_co2, 6)

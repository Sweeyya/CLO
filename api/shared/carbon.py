# api/shared/carbon.py
import requests

def get_regional_intensity_if_available(region: str = "us-east") -> float:
    """
    Returns carbon intensity (kg CO2 per kWh) for a given region.
    In a future update, this can fetch live data from WattTime or ElectricityMaps.
    """
    mapping = {
        "us-east": 0.35,
        "us-west": 0.40,
        "eu-central": 0.20,
        "norway": 0.02,
        "india": 0.55,
        "china": 0.70
    }

    try:
        # This placeholder simulates real lookup; later you can replace it with a live API call
        return mapping.get(region, 0.35)
    except Exception:
        # Fallback to default intensity if anything fails
        return 0.35


def calculate_carbon(energy_kwh: float, region: str = "us-east") -> float:
    """
    Calculates CO2 emissions based on regional grid intensity.
    Returns kilograms (kg) of CO2 emitted.
    """
    intensity = get_regional_intensity_if_available(region)
    return round(energy_kwh * intensity, 9)

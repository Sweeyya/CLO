# Water intensity values (liters per kWh) by region, based on weighted averages
# of dominant power sources. Source: Macknick et al. 2012, NREL.
# TODO: Replace with real-time power mix data from Electricity Maps power
# breakdown endpoint when available.
WATER_INTENSITY_MAP = {
    "us-east": 1.1,    # heavy natural gas + some coal
    "us-west": 0.5,    # more solar and wind
    "eu-central": 0.8, # mixed gas, wind, coal
    "norway": 0.01,    # almost all hydroelectric
    "india": 1.5,      # heavy coal
    "china": 1.6,      # heavy coal
}

DEFAULT_WATER_INTENSITY = 1.0


def get_water_intensity(region: str) -> float:
    """Return liters of water per kWh for the given region."""
    return WATER_INTENSITY_MAP.get(region, DEFAULT_WATER_INTENSITY)


def calculate_water(energy_kwh: float, region: str) -> float:
    """
    Estimate water consumption (liters) for an inference request.
    Formula: energy_kwh * liters_per_kwh
    """
    return round(energy_kwh * get_water_intensity(region), 6)

"""
Utility functions to convert different units.
Specially useful whrn working with dataframes.
"""


def feet_to_meter(feet) -> float:
    return float(feet) * 0.3048


def meter_to_feet(meter) -> float:
    return float(meter) / 0.3048

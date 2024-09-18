"""
Utility functions to convert different units.
Specially useful whrn working with dataframes.
"""


def feet_to_meter(feet, decimals=4) -> float:
    return round(float(feet) * 0.3048, decimals)


def meter_to_feet(meter, decimals=4) -> float:
    return round(float(meter) / 0.3048, decimals)

from wellbelog.utils.units import feet_to_meter, meter_to_feet


def test_feet_to_meter():
    assert feet_to_meter(1, 1) == 0.3
    assert feet_to_meter(2, 1) == 0.6


def test_meter_to_feet():
    assert meter_to_feet(1, 1) == 3.3
    assert meter_to_feet(2, 1) == 6.6

from motorgeek.core.analysis import (
    calculate_power_to_weight,
    calculate_hp_per_liter,
    calculate_msrp_inflation_adj,
)

def test_calculate_power_to_weight():
    result = calculate_power_to_weight(355, 1550)
    assert abs(result - 229.0) < 0.1

def test_calculate_hp_per_liter():
    result = calculate_hp_per_liter(355, 3600)
    assert abs(result - 98.6) < 0.1

def test_msrp_inflation_adj():
    result = calculate_msrp_inflation_adj(30000, 1998, 2026)
    assert result > 30000
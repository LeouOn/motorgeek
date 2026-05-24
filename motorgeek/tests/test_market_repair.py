from datetime import datetime
from motorgeek.core.models import MarketHistory, RepairCosts

def test_market_history_fields():
    mh = MarketHistory(
        car_id=1,
        date_recorded=datetime(2026, 1, 1),
        price_low=15000,
        price_high=20000,
        market_trend_indicator="stable",
        source_site="BringATrailer"
    )
    assert mh.price_low == 15000
    assert mh.price_high == 20000

def test_repair_costs_fields():
    rc = RepairCosts(
        car_id=1,
        repair_name="Timing chain tensioner",
        repair_category="engine",
        total_cost=850.0,
        parts_cost=450.0,
        labor_cost=400.0,
        currency="USD",
        shop_type="independent",
        source="RepairPal"
    )
    assert rc.total_cost == 850.0
    assert rc.repair_category == "engine"
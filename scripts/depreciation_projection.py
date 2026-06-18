"""Depreciation projection tool for MotorGeek bottom-buyer analysis.

Projects 20-year value curve for any car, identifies sweet spot / caution / danger zones,
and flags maintenance cliffs from known reliability issues.

Usage:
  python scripts/depreciation_projection.py <car_id> [--years 20]
"""

import sqlite3, sys, math

DB = "data/motorgeek.db"

# Default annual depreciation rates by segment (used when depreciation_5yr_pct is NULL)
SEGMENT_RATES = {
    "luxury_flagship": 0.13,   # A8, S-Class, 7 Series — ~50% after 5yr (observed)
    "luxury_midsize": 0.11,    # 5 Series, E-Class — ~45% after 5yr
    "mainstream": 0.09,        # Camry, Accord — ~38% after 5yr
    "truck_suv": 0.07,         # 4Runner, Tundra — ~30% after 5yr
    "ev": 0.18,                # Taycan, e-tron — ~63% after 5yr
    "collector_appreciating": 0.03,  # Already-appreciating classics
    "default": 0.12,           # catch-all — ~48% after 5yr
}


def classify_segment(car: dict) -> str:
    """Infer depreciation segment from car attributes."""
    make = car["make"].lower()
    model = car["model"].lower()
    body = (car.get("body_style") or "").lower()
    variant = (car.get("variant") or "").lower()
    era = (car.get("era_tag") or "").lower()
    hp = car.get("horsepower_bhp") or 0

    if body in ("suv", "truck", "minivan") and make in ("toyota", "lexus", "honda"):
        return "truck_suv"
    if make in ("toyota", "lexus") and body == "suv":
        return "truck_suv"
    if any(ev in (variant + " " + car.get("character", "")) for ev in ("electric", "ev", "taycan", "model")):
        return "ev"
    if make in ("porsche",) and "taycan" in variant:
        return "ev"
    # Collector cars: >20 years old + high reliability = appreciating, not depreciating
    if (car.get("reliability_score") or 0) > 80 and (car.get("year_start") or 9999) < 2006:
        return "collector_appreciating"
    if make in ("lexus", "toyota", "honda", "acura", "subaru") and (era == "classic" or (car.get("year_start") or 9999) < 2006):
        return "collector_appreciating"
    
    if make in ("mercedes-benz", "bmw", "audi") and model in ("s-class", "7 series", "a8", "s550", "560sel"):
        return "luxury_flagship"
    if make in ("lexus",) and model in ("ls", "ls 400", "lx"):
        return "luxury_flagship"
    if make in ("mercedes-benz", "bmw", "audi", "cadillac", "genesis", "volvo", "lexus"):
        return "luxury_midsize"
    if hp > 400 and make in ("toyota",) and model in ("tundra",):
        return "truck_suv"
    return "mainstream"


def load_car(db: sqlite3.Connection, car_id: int) -> dict:
    row = db.execute("""
        SELECT c.make, c.model, c.variant, c.year_start, c.generation,
               c.body_style, c.character, c.era_tag,
               pi.horsepower_bhp, pi.engine_layout,
               cto.msrp_original, cto.depreciation_5yr_pct,
               cto.annual_maintenance_est,
               r.reliability_score, b.q_score,
               r.known_issues
        FROM cars c
        LEFT JOIN powertrain_ice pi ON c.id = pi.car_id
        LEFT JOIN cost_to_own cto ON c.id = cto.car_id
        LEFT JOIN reliability r ON c.id = r.car_id
        LEFT JOIN build_quality b ON c.id = b.car_id
        WHERE c.id = ?
    """, (car_id,)).fetchone()
    if not row:
        return None
    cols = ["make","model","variant","year_start","generation","body_style","character","era_tag",
            "horsepower_bhp","engine_layout","msrp_original","depreciation_5yr_pct",
            "annual_maintenance_est","reliability_score","q_score","known_issues"]
    return dict(zip(cols, row))


def get_annual_rate(car: dict) -> float:
    """Get annual depreciation rate, falling back to segment defaults."""
    d5 = car.get("depreciation_5yr_pct")
    if d5 and d5 > 0:
        return 1 - (1 - d5 / 100) ** (1 / 5)
    segment = classify_segment(car)
    return SEGMENT_RATES.get(segment, SEGMENT_RATES["default"])


def project_curve(msrp: float, annual_rate: float, years: int = 20) -> list[dict]:
    """Generate year-by-year value projections using smooth exponential decay."""
    curve = []
    for y in range(years + 1):
        # Smooth decay: early years faster, tapering over time
        effective_rate = annual_rate * (1.4 - 0.03 * min(y, 15))
        value = max(msrp * 0.04, msrp * (1 - effective_rate) ** y)
        pct_msrp = round(value / msrp * 100, 1) if msrp else 0

        if pct_msrp > 55:
            zone = "DEPRECIATING"
        elif pct_msrp > 25:
            zone = "SWEET SPOT"
        elif pct_msrp > 10:
            zone = "CAUTION"
        else:
            zone = "FLOOR"

        curve.append({"year": y, "value": round(value), "pct_msrp": pct_msrp, "zone": zone})
    return curve


def extract_milestones(known_issues_json: str) -> list[str]:
    """Extract mileage-based maintenance milestones."""
    import json
    milestones = []
    if not known_issues_json:
        return milestones
    try:
        issues = json.loads(known_issues_json)
    except (json.JSONDecodeError, TypeError):
        return milestones
    for issue in issues:
        if isinstance(issue, str):
            s = issue.lower()
            if "80k" in s or "100k" in s or "120k" in s or "150k" in s:
                milestones.append(issue[:120])
    return milestones


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/depreciation_projection.py <car_id> [--years 20]")
        sys.exit(1)

    car_id = int(sys.argv[1])
    years = 20
    for i, arg in enumerate(sys.argv):
        if arg == "--years" and i + 1 < len(sys.argv):
            years = int(sys.argv[i + 1])

    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    car = load_car(db, car_id)
    if not car:
        print(f"Car {car_id} not found.")
        sys.exit(1)

    msrp = car.get("msrp_original")
    if not msrp:
        print(f"⚠ No MSRP in cost_to_own for car {car_id}. Using segment-based projection.")
        msrp = 60000  # reasonable default

    annual_rate = get_annual_rate(car)
    segment = classify_segment(car)

    print(f"\n{'='*70}")
    print(f"  {car['make']} {car['model']} {car['variant'] or ''}")
    print(f"  {car['generation'] or ''}  ({car['year_start']})")
    print(f"  Engine: {car['engine_layout'] or 'unknown'}")
    print(f"  MSRP: ${msrp:,.0f}   |   Segment: {segment}")
    if car.get("depreciation_5yr_pct"):
        print(f"   5yr depreciation: {car['depreciation_5yr_pct']:.0f}%   |   Annual rate: {annual_rate*100:.1f}%")
    else:
        print(f"   Depreciation rate: ~{annual_rate*100:.1f}%/yr (segment estimate)")
    if car.get("reliability_score"):
        print(f"   Reliability: {car['reliability_score']:.1f}   |   Q-score: {car.get('q_score', '?'):.1f}")
    print(f"{'='*70}")

    curve = project_curve(msrp, annual_rate, years)

    print(f"\n{'Year':>4}  {'Value':>10}  {'%MSRP':>6}  {'Zone':<20}")
    print(f"{'─'*4}  {'─'*10}  {'─'*6}  {'─'*20}")
    for pt in curve:
        marker = " <--" if pt["zone"] == "SWEET SPOT" else ""
        print(f"{pt['year']:>4}  ${pt['value']:>9,}  {pt['pct_msrp']:>5.0f}%  {pt['zone']:<20}{marker}")

    # Maintenance milestones
    milestones = extract_milestones(car.get("known_issues", ""))
    if milestones:
        print(f"\n-- Known maintenance cliffs from reliability data:")
        for m in milestones[:6]:
            print(f"   * {m}")

    # Summary
    sweet = [pt for pt in curve if pt["zone"] == "SWEET SPOT"]
    if sweet:
        low = sweet[0]
        high = sweet[-1]
        age_now = 2026 - car["year_start"]
        years_to_go = max(0, low["year"] - age_now)
        sweet_start_yr = low["year"] + car["year_start"]
        sweet_end_yr = high["year"] + car["year_start"]
        
        if age_now > high["year"]:
            print(f"\n--- SWEET SPOT: age {low['year']}-{high['year']} (years {sweet_start_yr}-{sweet_end_yr})")
            print(f"   Projected value at time: ${low['value']:,} - ${high['value']:,}")
            if age_now > 20:
                print(f"   Sweet spot was in the past -- this car may be appreciating as a collector")
            elif age_now > 15:
                print(f"   Sweet spot was in the past -- near the floor, maintenance costs dominate")
            else:
                print(f"   Sweet spot was in the past -- now in caution zone (maintenance cliffs ahead)")
            print(f"   Current age: {age_now}. Appreciation may be underway.")
        else:
            print(f"\n--- SWEET SPOT: age {low['year']}-{high['year']} (years {sweet_start_yr}-{sweet_end_yr})")
            print(f"   Projected value: ${low['value']:,} - ${high['value']:,}")
            print(f"   Depreciated: {100-low['pct_msrp']:.0f}% - {100-high['pct_msrp']:.0f}% from MSRP")
            if years_to_go > 0:
                print(f"   Sweet spot begins in ~{years_to_go} years")
            else:
                print(f"   >> Currently IN sweet spot <<")

    db.close()


if __name__ == "__main__":
    main()

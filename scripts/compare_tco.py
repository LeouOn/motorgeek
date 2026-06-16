"""TCO comparison tool — total cost of ownership over N years.

Compares multiple cars on purchase price, fuel, maintenance, and depreciation.
Integrates maintenance cliff costs from reliability data.

Usage:
  python scripts/compare_tco.py <car_id1> <car_id2> [car_id3...] [--years 5] [--miles_per_year 12000]
"""

import sqlite3, sys, json

DB = "data/motorgeek.db"
FUEL_PRICE = 4.50  # $/gallon (2026 US avg premium/regular blended)


def load_car(db: sqlite3.Connection, car_id: int) -> dict:
    row = db.execute("""
        SELECT c.make, c.model, c.variant, c.year_start,
               pi.horsepower_bhp, pi.curb_weight_kg, pi.engine_layout,
               cto.msrp_original, cto.fuel_econ_city_mpg, cto.fuel_econ_hwy_mpg,
               cto.annual_maintenance_est, cto.depreciation_5yr_pct,
               r.reliability_score, b.q_score,
               r.known_issues, r.common_failures
        FROM cars c
        LEFT JOIN powertrain_ice pi ON c.id = pi.car_id
        LEFT JOIN cost_to_own cto ON c.id = cto.car_id
        LEFT JOIN reliability r ON c.id = r.car_id
        LEFT JOIN build_quality b ON c.id = b.car_id
        WHERE c.id = ?
    """, (car_id,)).fetchone()
    if not row:
        return None
    cols = ["make","model","variant","year_start","horsepower_bhp","curb_weight_kg",
            "engine_layout","msrp_original","fuel_econ_city_mpg","fuel_econ_hwy_mpg",
            "annual_maintenance_est","depreciation_5yr_pct","reliability_score","q_score",
            "known_issues","common_failures"]
    return dict(zip(cols, row))


def get_current_value(db: sqlite3.Connection, car_id: int) -> float | None:
    """Get most recent market value (midpoint of price range)."""
    row = db.execute("""
        SELECT price_low, price_high FROM market_history
        WHERE car_id = ? ORDER BY date_recorded DESC LIMIT 1
    """, (car_id,)).fetchone()
    if row and row[0] and row[1]:
        return (row[0] + row[1]) / 2
    return None


def estimate_current_value(car: dict, db: sqlite3.Connection, car_id: int) -> float:
    """Estimate current market value: actual data > depreciation projection > MSRP fallback."""
    actual = get_current_value(db, car_id)
    if actual:
        return actual

    # Fallback: project from MSRP using 5yr depreciation rate
    msrp = car.get("msrp_original") or 60000
    age = 2026 - car["year_start"]
    d5 = car.get("depreciation_5yr_pct")
    if d5 and d5 > 0:
        annual_rate = 1 - (1 - d5 / 100) ** (1 / 5)
    else:
        # Segment-based fallback
        if car.get("reliability_score", 0) > 80 and age < 10:
            annual_rate = 0.09
        else:
            annual_rate = 0.13
    return max(msrp * 0.05, msrp * (1 - annual_rate) ** age)


def extract_milestone_costs(known_issues_json: str) -> list[tuple[int, float]]:
    """Extract mileage and cost from known_issues JSON."""
    milestones = []
    if not known_issues_json:
        return milestones
    try:
        issues = json.loads(known_issues_json)
    except (json.JSONDecodeError, TypeError):
        return milestones

    import re
    for issue in issues:
        if not isinstance(issue, str):
            continue
        costs = re.findall(r'\$?(\d[\d,]+)-?\$?(\d[\d,]*)\s*(?:total|each|shop|indie|replacement|repair)?', issue.lower())
        if costs:
            low = int(costs[0][0].replace(",", ""))
            high = int(costs[0][1].replace(",", "")) if costs[0][1] else low
            avg_cost = (low + high) / 2
            k_match = re.search(r'(\d+)[kK]', issue)
            if k_match:
                mile_mark = int(k_match.group(1)) * 1000
                milestones.append((mile_mark, avg_cost))
    return milestones


def main():
    car_ids = []
    years = 5
    miles_per_year = 12000

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--years" and i + 1 < len(sys.argv):
            years = int(sys.argv[i + 1])
            i += 2
        elif arg == "--miles" and i + 1 < len(sys.argv):
            miles_per_year = int(sys.argv[i + 1])
            i += 2
        else:
            try:
                car_ids.append(int(arg))
            except ValueError:
                pass
            i += 1

    if len(car_ids) < 1:
        print("Usage: python scripts/compare_tco.py <car_id1> <car_id2> ... [--years 5] [--miles 12000]")
        sys.exit(1)

    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row

    cars = []
    for cid in car_ids:
        car = load_car(db, cid)
        if car:
            car["id"] = cid
            car["current_value"] = estimate_current_value(car, db, cid)
            cars.append(car)

    if not cars:
        print("No valid cars found.")
        sys.exit(1)

    total_miles = miles_per_year * years

    print(f"\n  TCO Comparison -- {years} years, {miles_per_year:,} mi/yr ({total_miles:,} total mi), ${FUEL_PRICE}/gal")
    print(f"  {'='*80}")

    results = []
    for car in cars:
        purchase = car["current_value"]
        city = car.get("fuel_econ_city_mpg") or 0
        hwy = car.get("fuel_econ_hwy_mpg") or 0
        avg_mpg = (city + hwy) / 2 if city and hwy else 25
        if avg_mpg == 0:
            avg_mpg = 25

        # For EVs: if city/hwy are > 50, they're MPGe — convert to cost/mile differently
        if avg_mpg > 50:
            fuel_cost = (total_miles / avg_mpg) * (FUEL_PRICE / 3.5)  # ~$1.50/100mi
        else:
            fuel_cost = (total_miles / avg_mpg) * FUEL_PRICE

        maint = (car.get("annual_maintenance_est") or 800) * years

        # Maintenance cliff costs: if the car hits milestone mileage within ownership period
        start_miles = (2026 - car["year_start"]) * miles_per_year
        cliff_total = 0
        milestones = extract_milestone_costs(car.get("known_issues", ""))
        for mile_mark, cost in milestones:
            if start_miles < mile_mark < start_miles + total_miles:
                cliff_total += cost

        # Depreciation: project remaining value after N years
        annual_rate = 0.10
        d5 = car.get("depreciation_5yr_pct")
        if d5 and d5 > 0:
            annual_rate = 1 - (1 - d5 / 100) ** (1 / 5)
        future_value = purchase * (1 - annual_rate) ** years
        depreciation = purchase - future_value

        total = purchase + fuel_cost + maint + cliff_total + depreciation

        results.append({
            "car": car,
            "purchase": purchase,
            "fuel": fuel_cost,
            "maint": maint,
            "cliffs": cliff_total,
            "depreciation": depreciation,
            "total": total,
            "avg_mpg": avg_mpg,
        })

    # Sort by total cost
    results.sort(key=lambda r: r["total"])

    for i, r in enumerate(results):
        car = r["car"]
        per_mile = r["total"] / total_miles if total_miles > 0 else 0
        header = f"  {'='*80}"
        print(f"\n  {car['make']} {car['model']} {car['variant'] or ''} ({car['year_start']})")
        print(f"  Engine: {car.get('engine_layout') or '?'}  |  HP: {car.get('horsepower_bhp') or '?'}  |  MPG: {r['avg_mpg']:.0f}")
        print(f"  Rel: {car.get('reliability_score','?')}   Q: {car.get('q_score','?')}   MSRP: ${car.get('msrp_original','?'):,.0f}")
        print(f"  {'-'*70}")
        print(f"  Purchase price:         ${r['purchase']:>10,.0f}")
        print(f"  Fuel ({r['avg_mpg']:.0f} MPG):           ${r['fuel']:>10,.0f}")
        print(f"  Maintenance ({years}yr):     ${r['maint']:>10,.0f}")
        if r['cliffs'] > 0:
            print(f"  Maint cliffs (est):      ${r['cliffs']:>10,.0f}")
        print(f"  Depreciation loss:       ${r['depreciation']:>10,.0f}")
        print(f"  {'-'*70}")
        print(f"  TOTAL ({years}yr):           ${r['total']:>10,.0f}")
        print(f"  Per mile:                ${per_mile:>.2f}/mi")

        # Show biggest cost driver
        costs = [
            ("Purchase price", r["purchase"]),
            ("Fuel", r["fuel"]),
            ("Maintenance", r["maint"] + r["cliffs"]),
            ("Depreciation", r["depreciation"]),
        ]
        costs.sort(key=lambda x: x[1], reverse=True)
        print(f"  Biggest cost: {costs[0][0]} (${costs[0][1]:,.0f})")
        print()

    # Summary ranking
    print(f"  {'='*80}")
    print(f"  RANKING (lowest total cost first)")
    print(f"  {'-'*60}")
    for i, r in enumerate(results):
        car = r["car"]
        print(f"  {i+1}. {car['make']} {car['model']} {car.get('variant','')} -- ${r['total']:,.0f} total (${r['total']/total_miles:.2f}/mi)")

    db.close()


if __name__ == "__main__":
    main()

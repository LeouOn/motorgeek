#!/usr/bin/env python3
"""
BOTTOM-BUYER TCO ANALYZER
For the contrarian who buys at the bottom of depreciation and extracts the last 30K miles.

Philosophy: Find cars where someone else ate the depreciation, the engineering is proven,
and 30K more miles is within the reliable window. Cheapest thrills per mile.

Formula:
  - Used price estimated from current market (depreciated to near-bottom)
  - Fuel cost = (30K / combined MPG) * fuel price
  - Maintenance estimated for 30K miles at the car's age/mileage
  - Risk buffer = probability-weighted catastrophic failure cost
  - $/mile = (used_price + fuel + maint + risk) / 30000
  - Power score = HP / $/mile (more HP per dollar = better)
  - Fun factor = reliability * HP / $/mile (the holy trinity)
"""

import json

# Combined MPG estimate
def combined_mpg(city, hwy):
    if not city or not hwy:
        return None
    return 0.55 * city + 0.45 * hwy

# Fuel type: most NA engines run regular, most turbos require premium
# Exceptions noted
def fuel_price(car):
    name = car['name'].lower()
    aspir = car.get('aspiration', '').lower()
    fuel_sys = car.get('fuel_system', '').lower()
    
    # Regular gas (87 octane)
    regular_cars = ['ls 400', 'ls430', 'ls 430', 'es 350', 'g80 3.8', 'g80 5.0', 'g90 5.0',
                    'camry', 'k5', 'glk', 'c300 w204']
    for rc in regular_cars:
        if rc in name:
            return 3.20
    
    # Premium required (91+)
    premium_cars = ['bmw', 'porsche', 'ferrari', 'mercedes', 'amg', 'audi', 'volvo',
                    's2000', 'supra', 'stinger', 'g70', 'g90 2nd', 'gv70', 'gv80',
                    'q50', 'c450', 'c400', 'e450', 'ls460', 'ls600']
    for pc in premium_cars:
        if pc in name:
            return 3.80
    
    # Default: NA = regular, turbo/supercharged = premium
    if 'naturally' in aspir or 'na' in aspir:
        return 3.20
    return 3.80

# Estimate current used price for bottom-buyer
# Based on: age, original MSRP, depreciation curve, reliability
def estimate_used_price(car):
    """Estimate what a contrarian bottom-buyer would pay today"""
    import datetime
    current_year = 2026
    
    year_start = car.get('year_start', 2020)
    year_end = car.get('year_end') or car.get('year_start', 2020)
    age = current_year - year_end  # years since production ended
    msrp = car.get('msrp', 50000)
    score = car.get('score', 70)
    hp = car.get('hp', 300)
    
    # Base depreciation curve (percentage of MSRP retained)
    # Reliable cars hold value better
    if age <= 0:
        base_pct = 0.85
    elif age <= 3:
        base_pct = 0.55
    elif age <= 5:
        base_pct = 0.40
    elif age <= 8:
        base_pct = 0.25
    elif age <= 12:
        base_pct = 0.15
    elif age <= 20:
        base_pct = 0.10
    elif age <= 30:
        base_pct = 0.08
    else:
        base_pct = 0.05  # classic/collector territory
    
    # Reliability premium: high-score cars hold 5-15% more value
    reliability_adj = (score - 70) / 100 * 0.15
    
    # HP premium: high-HP cars hold value better (enthusiast demand)
    hp_adj = min(hp / 5000, 0.10)
    
    # Special adjustments for known market quirks
    name = car.get('name', '').lower()
    special_adj = 0
    if 's2000' in name: special_adj = 0.25  # S2000s are collector-priced
    if 'supra' in name and 'a80' in name: special_adj = 0.40  # MK4 Supra insane market
    if 'ls400' in name or 'ls 400' in name: special_adj = 0.10  # JDM tax
    if '500e' in name: special_adj = 0.30  # Porsche-built Mercedes
    if '300 sl' in name or 'gullwing' in name: special_adj = 1.50  # Museum piece
    if '190 sl' in name: special_adj = 0.60  # Collector
    if 'pagoda' in name: special_adj = 0.50  # Collector
    if 'f355' in name: special_adj = 0.25  # Ferrari tax
    if 'm3 e46' in name: special_adj = 0.20  # E46 M3 tax
    if '560 sl' in name: special_adj = 0.30  # R107 tax
    if 'sl 600 r129' in name: special_adj = 0.25
    if '996' in name: special_adj = 0.15  # 996 turbo starting to appreciate
    if 'polestar' in name or 'v60' in name: special_adj = 0.05  # Enthusiast niche
    
    pct = min(base_pct + reliability_adj + hp_adj + special_adj, 0.95)
    return max(round(msrp * pct, -2), 2000)

# Estimate max reliable mileage (where you'd still buy it)
def max_reliable_miles(car):
    """Realistic upper bound where the car is still a responsible buy"""
    score = car.get('score', 70)
    name = car.get('name', '').lower()
    aspir = car.get('aspiration', '').lower()
    
    base = 150  # base 150K for any modern car
    
    # Score adjustments
    if score >= 88: base = 250
    elif score >= 83: base = 220
    elif score >= 78: base = 200
    elif score >= 73: base = 180
    elif score >= 68: base = 160
    else: base = 140
    
    # Aspiration penalty: turbos have more failure points at high mileage
    if 'twin-turbo' in aspir or 'biturbo' in aspir: base -= 20
    elif 'turbo' in aspir and 'naturally' not in aspir: base -= 10
    if 'supercharged' in aspir: base -= 15
    
    # Special cases
    if 'ls 400' in name or 'ls400' in name: base = 300  # Legendary
    if 'ls430' in name or 'ls 430' in name: base = 280
    if 'es 350' in name: base = 250
    if 'ls460' in name: base = 180  # Trans issues cap it
    if 'ls600' in name or '600h' in name: base = 150  # Hybrid complexity
    if 'g90 5.0' in name or 'g80 5.0' in name: base = 170  # Tau parts concern
    if 'tau' in car.get('variant', '').lower() or '5.0 v8' in name: base = 170
    if 'camry' in name: base = 250  # Camry is Camry
    if 's2000' in name: base = 220  # Overbuilt
    if 'supra' in name and 'a80' in name: base = 200  # 2JZ but old
    if 'm3 e46' in name: base = 170  # Subframe + VANOS
    if '500e' in name: base = 160  # Porsche maintenance, old
    if 'pagoda' in name or '190 sl' in name: base = 999  # Classics, miles don't matter
    if '300 sl' in name: base = 999
    if '560 sl' in name: base = 999
    if 'sl 600' in name: base = 999
    if 'f355' in name: base = 150  # Ferrari, always risky
    
    return min(base, 999)

# Risk buffer: probability-weighted catastrophic failure cost
def risk_buffer(car):
    """Expected value of worst-case failure over 30K miles"""
    score = car.get('score', 70)
    ease = car.get('ease', 70)
    name = car.get('name', '').lower()
    
    # Base probability of catastrophic failure in 30K miles
    # Score 90+ = 5%, 80+ = 10%, 70+ = 15%, 60+ = 25%, <60 = 35%
    if score >= 90: prob = 0.05
    elif score >= 85: prob = 0.08
    elif score >= 80: prob = 0.10
    elif score >= 75: prob = 0.15
    elif score >= 70: prob = 0.20
    elif score >= 65: prob = 0.25
    else: prob = 0.35
    
    # Ease of repair affects cost, not probability
    ease = car.get('ease', 70)
    if ease >= 85: repair_cost = 3000
    elif ease >= 75: repair_cost = 5000
    elif ease >= 65: repair_cost = 7000
    elif ease >= 55: repair_cost = 9000
    else: repair_cost = 12000
    
    # Special cases
    if 'ls600' in name or '600h' in name: repair_cost = 15000  # Hybrid battery + trans
    if 'f355' in name: repair_cost = 15000  # Ferrari parts
    if '500e' in name: repair_cost = 12000  # Porsche-only parts
    if 'g80 5.0' in name or 'g90 5.0' in name: repair_cost = 8000  # Parts backorder
    if 'pagoda' in name or '190 sl' in name or '300 sl' in name: repair_cost = 5000  # Classics are fixable
    if '560 sl' in name or 'sl 600' in name: repair_cost = 5000
    
    return round(prob * repair_cost)

# Import cars from the DB export
cars_raw = []
import sys
import os

# Read directly from SQLite DB
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..', 'data', 'motorgeek.db')
db_path = os.path.normpath(db_path)

if os.path.exists(db_path):
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.make, c.model, c.generation, c.year_start, c.year_end,
               COALESCE(c.variant, '') as variant,
               r.reliability_score as score,
               r.score_engine, r.score_ease_of_repair,
               ct.fuel_econ_city_mpg, ct.fuel_econ_hwy_mpg, ct.annual_maintenance_est,
               ct.msrp_original,
               pi.horsepower_bhp, pi.displacement_cc, pi.aspiration, pi.curb_weight_kg,
               pi.fuel_system, pi.transmission_type
        FROM cars c
        LEFT JOIN reliability r ON r.car_id = c.id
        LEFT JOIN cost_to_own ct ON ct.car_id = c.id
        LEFT JOIN powertrain_ice pi ON pi.car_id = c.id
        WHERE r.reliability_score IS NOT NULL
        AND pi.horsepower_bhp IS NOT NULL
        AND ct.fuel_econ_city_mpg IS NOT NULL
        ORDER BY r.reliability_score DESC
    """)
    rows = cur.fetchall()
    conn.close()
    
    for row in rows:
        cars_raw.append({
            'id': row['id'],
            'make': row['make'],
            'model': row['model'],
            'generation': row['generation'] or '',
            'year_start': row['year_start'] or 2020,
            'year_end': row['year_end'],
            'variant': row['variant'] or '',
            'score': row['score'] or 70,
            'ease': row['score_ease_of_repair'] if row['score_ease_of_repair'] else 70,
            'city_mpg': row['fuel_econ_city_mpg'] or 20,
            'hwy_mpg': row['fuel_econ_hwy_mpg'] or 28,
            'maint': row['annual_maintenance_est'] or 800,
            'msrp': row['msrp_original'] or 50000,
            'hp': row['horsepower_bhp'] or 250,
            'disp': row['displacement_cc'] or 2000,
            'aspiration': (row['aspiration'] or '').lower(),
            'weight': row['curb_weight_kg'] or 1700,
            'fuel_system': (row['fuel_system'] or '').lower(),
            'trans': (row['transmission_type'] or '').lower(),
        })

# If no file, use hardcoded data
if not cars_raw:
    print("WARNING: No DB file found, using hardcoded sample")
    cars_raw = [
        {'id': 63, 'make': 'Lexus', 'model': 'LS 400', 'generation': 'first', 'year_start': 1989, 'year_end': 1994, 'variant': '400', 'score': 92.0, 'city_mpg': 16, 'hwy_mpg': 22, 'maint': 400, 'msrp': 35000, 'hp': 250, 'disp': 3969, 'aspiration': 'naturally aspirated', 'weight': 1685, 'fuel_system': 'MPI', 'trans': '4-speed auto'},
        {'id': 39, 'make': 'Lexus', 'model': 'LS', 'generation': '3rd gen', 'year_start': 2001, 'year_end': 2006, 'variant': 'LS430', 'score': 88.5, 'city_mpg': 17, 'hwy_mpg': 24, 'maint': 450, 'msrp': 55000, 'hp': 290, 'disp': 4293, 'aspiration': 'NA', 'weight': 1660, 'fuel_system': 'MPI', 'trans': '5-speed auto'},
    ]

# Build analysis
results = []
for c in cars_raw:
    name = f"{c['make']} {c['model']} {c['variant']}".strip()
    c['name'] = name
    
    mpg = combined_mpg(c['city_mpg'], c['hwy_mpg']) or 20
    fp = fuel_price(c)
    used = estimate_used_price(c)
    max_life = max_reliable_miles(c)
    
    # Buy odometer: 70% of max life (buy with some life left)
    buy_odo = int(max_life * 0.7)
    
    # 30K miles of driving
    miles = 30000
    fuel_cost = (miles / mpg) * fp
    
    # Maintenance for 30K at this car's age
    age = 2026 - (c.get('year_end') or c.get('year_start', 2020))
    maint_30k = c['maint'] * 2.5  # ~2.5 years of driving 12K/yr
    if age > 15: maint_30k *= 1.3  # older cars need more
    if age > 25: maint_30k *= 1.2  # classics even more
    
    risk = risk_buffer(c)
    
    total = used + fuel_cost + maint_30k + risk
    cost_per_mile = total / miles
    
    # Power-per-dollar
    hp_per_dollar = c['hp'] / cost_per_mile
    
    # Fun factor: reliability * HP / cost_per_mile
    fun = c['score'] * c['hp'] / cost_per_mile
    
    # Is it within reliable window?
    reliable = buy_odo + 30 <= max_life  # can we get 30K more?
    
    results.append({
        'name': name,
        'make': c['make'],
        'year': f"{c['year_start']}-{c.get('year_end', '?')}",
        'score': c['score'],
        'hp': int(c['hp']),
        'mpg': round(mpg, 1),
        'fuel': 'regular' if fp < 3.50 else 'premium',
        'used_price': used,
        'buy_odo': f"{buy_odo}K",
        'max_life': f"{max_life}K",
        'fuel_30k': round(fuel_cost),
        'maint_30k': round(maint_30k),
        'risk': risk,
        'total': round(total),
        'cost_per_mile': round(cost_per_mile, 2),
        'hp_per_dollar': round(hp_per_dollar, 1),
        'fun': round(fun, 1),
        'reliable': reliable,
    })

# Sort by cost_per_mile (best value first)
results.sort(key=lambda x: x['cost_per_mile'])

print("=" * 130)
print("BOTTOM-BUYER TCO: ALL SCORED CARS (250+ HP) -- Ranked by $/mile")
print("Strategy: Buy at 70% of max reliable miles, extract 30K more miles")
print("=" * 130)
print()

# Print header
hdr = f"{'#':>2} {'Car':30s} {'Year':>10s} {'Score':>5s} {'HP':>5s} {'MPG':>5s} {'Fuel':>7s} {'Buy$':>7s} {'Buy@':>6s} {'Max':>5s} {'Gas':>5s} {'Mnt':>5s} {'Risk':>5s} {'Total':>7s} {'$/mi':>5s} {'HP/$':>6s} {'Fun':>7s}"
print(hdr)
print("-" * 130)

for i, r in enumerate(results, 1):
    flag = " " if r['reliable'] else "!"  # ! = outside reliable window
    print(f"{flag}{i:>2} {r['name']:30s} {r['year']:>10s} {r['score']:>5.1f} {r['hp']:>5} {r['mpg']:>5.1f} {r['fuel']:>7s} ${r['used_price']:>6,} {r['buy_odo']:>6s} {r['max_life']:>5s} ${r['fuel_30k']:>4,} ${r['maint_30k']:>4,} ${r['risk']:>4,} ${r['total']:>6,} ${r['cost_per_mile']:>4.2f} {r['hp_per_dollar']:>6.1f} {r['fun']:>7.1f}")

print()
print("Legend: ! = outside reliable window (30K more exceeds max life estimate)")
print("        Buy$ = estimated used purchase price at bottom of depreciation")
print("        Buy@ = recommended odometer to buy at (70% of max reliable miles)")
print("        HP/$ = horsepower per dollar-per-mile (more = better)")
print("        Fun = reliability * HP / $/mile (the holy trinity)")

print()
print("=" * 130)
print("TOP 10 BY FUN FACTOR (reliability * HP / $ per mile)")
print("=" * 130)
print()

by_fun = sorted(results, key=lambda x: x['fun'], reverse=True)[:10]
for i, r in enumerate(by_fun, 1):
    print(f"{i:>2}. {r['name']:30s} | Score: {r['score']:.1f} | HP: {r['hp']} | ${r['cost_per_mile']:.2f}/mi | Fun: {r['fun']:.1f}")

print()
print("=" * 130)
print("TOP 10 CHEAPEST THRILLS (lowest $/mile with 250+ HP)")
print("=" * 130)
print()

cheap_thrills = sorted([r for r in results if r['hp'] >= 250 and r['reliable']], key=lambda x: x['cost_per_mile'])[:10]
for i, r in enumerate(cheap_thrills, 1):
    print(f"{i:>2}. {r['name']:30s} | ${r['used_price']:,} | {r['hp']}HP | {r['score']:.1f} | ${r['cost_per_mile']:.2f}/mi | {r['fuel']}")

"""Compare NEW MSRP vs estimated CURRENT USED price to identify:

  - APPRECIATING cars (worth more now than new): icons like 500E, E30 M3, etc.
  - FAST-DEPRECIATING cars (worth 50%+ less than new): modern luxury SUVs
"""
import sqlite3
import sys
from pathlib import Path

ROOT = Path('C:/Users/llama/OneDrive/proj/motorgeek')
sys.path.insert(0, str(ROOT))

from motorgeek.core.calculators.composite import compute_composite, compute_composite_v3
from motorgeek.core.calculators.practicality import compute_practicality_for_car_v2
from motorgeek.core.models import Car, Dimensions, PowertrainICE


def estimate_msrp(c):
    """Approximate original new MSRP for the car."""
    m, mo, yr = c['make'], c['model'], c['year']
    base = 30000
    if m == 'BMW':
        if any(x in mo for x in ('M3', 'M4', 'M5', 'M6', 'M8', 'X5 M', 'X6 M')):
            base = 90000
        elif 'M340i' in mo:
            base = 55000
        elif any(x in mo for x in ('X3', 'X4', '3 Series', '4 Series')):
            base = 45000
        elif any(x in mo for x in ('X5', 'X6', '5 Series', '7 Series')):
            base = 65000
        elif any(x in mo for x in ('X1', '2 Series')):
            base = 38000
        elif 'X7' in mo:
            base = 80000
        elif 'iX' in mo:
            base = 85000
        elif 'i4' in mo or 'i7' in mo:
            base = 65000
    elif m == 'Audi':
        if 'RS' in mo or 'RSQ8' in mo:
            base = 110000
        elif 'SQ' in mo:
            base = 65000
        elif 'A8' in mo:
            base = 90000
        elif any(x in mo for x in ('A6', 'A7', 'Q7', 'Q8')):
            base = 60000
        elif any(x in mo for x in ('A4', 'A5', 'Q5')):
            base = 45000
        elif 'Q3' in mo:
            base = 38000
        elif 'TT' in mo:
            base = 50000
        elif 'e-tron' in mo:
            base = 70000
    elif m == 'Mercedes-Benz':
        if 'AMG' in mo or 'Maybach' in mo:
            base = 110000
        elif any(x in mo for x in ('GLS', 'GLE', 'S-Class')):
            base = 80000
        elif 'GLC' in mo or 'G-Class' in mo or 'G550' in mo or 'G63' in mo:
            base = 130000
        elif any(x in mo for x in ('C-Class', 'E-Class', 'CLS')):
            base = 55000
        elif 'EQS' in mo or 'EQE' in mo:
            base = 105000
        elif 'GLK' in mo:
            base = 40000
    elif m == 'Lexus':
        if 'LX' in mo:
            base = 90000
        elif 'GX' in mo:
            base = 60000
        elif 'LS' in mo:
            base = 80000
        elif 'NX' in mo:
            base = 50000
        elif 'RX' in mo:
            base = 50000
        elif 'ES' in mo:
            base = 42000
        elif 'IS' in mo:
            base = 42000
        elif 'RC' in mo:
            base = 45000
    elif m == 'Porsche':
        if '911' in mo or 'GT3' in mo or 'Turbo' in mo:
            base = 120000
        elif 'Taycan' in mo:
            base = 90000
        elif 'Cayenne' in mo:
            base = 70000
        elif 'Macan' in mo:
            base = 55000
        elif '718' in mo or 'Cayman' in mo:
            base = 60000
        elif 'Panamera' in mo:
            base = 90000
    elif m == 'Genesis':
        if 'G90' in mo:
            base = 70000
        elif 'GV80' in mo:
            base = 50000
        elif 'G80' in mo or 'GV70' in mo:
            base = 48000
        elif 'G70' in mo:
            base = 38000
    elif m == 'Tesla':
        if 'Plaid' in mo:
            base = 135000
        elif 'Model S' in mo:
            base = 95000
        elif 'Model X' in mo:
            base = 100000
        elif 'Model 3' in mo:
            base = 45000
        elif 'Model Y' in mo:
            base = 55000
    elif m == 'Cadillac':
        if 'Escalade' in mo:
            base = 85000
        elif 'CT5' in mo:
            base = 50000
        elif 'CT6' in mo:
            base = 60000
        elif 'XT5' in mo:
            base = 45000
        elif 'XT4' in mo:
            base = 40000
        elif 'XT6' in mo:
            base = 50000
        elif 'Blackwing' in mo:
            base = 90000
        elif 'CTS-V' in mo:
            base = 85000
    elif m == 'Acura':
        if 'MDX' in mo:
            base = 50000
        elif 'RDX' in mo:
            base = 40000
        elif 'TLX' in mo:
            base = 40000
    elif m == 'Infiniti':
        if 'QX80' in mo:
            base = 70000
        elif 'QX60' in mo:
            base = 50000
        elif 'Q50' in mo:
            base = 40000
    elif m == 'Land Rover':
        if 'Range Rover' in mo:
            base = 100000
        elif 'Defender' in mo:
            base = 55000
        elif 'Discovery' in mo:
            base = 55000
        elif 'Evoque' in mo:
            base = 45000
    elif m == 'Honda':
        if 'Civic Type R' in mo:
            base = 45000
        else:
            base = 25000
    elif m == 'Toyota':
        if '4Runner' in mo:
            base = 40000
        elif 'Land Cruiser' in mo:
            base = 85000
        elif 'Supra' in mo:
            base = 55000
        else:
            base = 28000
    elif m == 'Mazda':
        base = 28000
    elif m == 'Subaru':
        if 'WRX' in mo:
            base = 32000
        else:
            base = 27000
    elif m == 'Volkswagen':
        if 'Golf' in mo:
            base = 28000
        else:
            base = 32000
    elif m == 'Hyundai':
        if 'Ioniq 5 N' in mo:
            base = 67000
        else:
            base = 30000
    elif m == 'Kia':
        base = 32000
    elif m == 'Ford':
        if 'Mustang' in mo or 'GT' in mo:
            base = 45000
        else:
            base = 35000
    elif m == 'Chevrolet':
        if 'Corvette' in mo:
            base = 65000
        elif 'Camaro' in mo:
            base = 45000
        else:
            base = 35000
    elif m == 'Dodge':
        if 'Challenger' in mo or 'Charger' in mo:
            base = 45000
        else:
            base = 35000
    elif m == 'Chrysler':
        if 'Pacifica' in mo:
            base = 40000
        else:
            base = 30000
    elif m == 'Nissan':
        if 'GT-R' in mo:
            base = 115000
        else:
            base = 28000
    elif m == 'Bentley':
        base = 200000
    elif m == 'Rolls-Royce':
        base = 350000
    elif m == 'Lamborghini':
        base = 220000
    elif m == 'Ferrari':
        base = 250000
    elif m == 'McLaren':
        base = 350000
    elif m == 'Maserati':
        base = 90000
    elif m == 'Alpine':
        base = 70000
    elif m == 'Jaguar':
        base = 55000
    elif m == 'Lincoln':
        if 'Navigator' in mo or 'Aviator' in mo:
            base = 75000
        else:
            base = 50000
    elif m == 'Buick':
        base = 35000
    elif m == 'Volvo':
        if 'XC90' in mo:
            base = 55000
        elif 'XC60' in mo:
            base = 45000
        elif 'EX90' in mo:
            base = 80000
        else:
            base = 40000
    elif m == 'VinFast':
        base = 50000
    elif m == 'Hongqi':
        base = 80000
    else:
        base = 35000

    if yr < 2010:
        return int(base * 0.7)
    elif yr < 2015:
        return int(base * 0.8)
    elif yr < 2018:
        return int(base * 0.88)
    elif yr < 2020:
        return int(base * 0.94)
    elif yr < 2022:
        return int(base * 0.98)
    else:
        return int(base * 1.0)


def estimate_used_value(c):
    """Estimate CURRENT used market value based on depreciation/appreciation patterns."""
    m, mo, yr = c['make'], c['model'], c['year']
    body = c.get('body')
    base = estimate_msrp(c)

    is_icon = (
        ('500E' in mo or 'E500' in mo or '560 SL' in mo or '500 SL' in mo or
         '300 SL' in mo or '190 SL' in mo) or
        (m == 'BMW' and 'M3' in mo and yr < 2010) or
        ('Civic Type R' in mo or 'NSX' in mo) or
        ('Skyline' in mo) or
        (m == 'Nissan' and 'GT-R' in mo and yr < 2018) or
        ('Land Cruiser' in mo and yr < 2020) or
        ('LFA' in mo or 'RC F' in mo or ('Supra' in mo and yr < 2020)) or
        (m == 'Porsche' and '911' in mo and yr < 1998) or
        ('RS6 Avant' in mo or 'RS2' in mo or 'RS4 Avant' in mo) or
        (m in ('Ferrari', 'Lamborghini', 'McLaren', 'Bentley', 'Rolls-Royce')) or
        # Italian supercars hold value
        (m == 'Maserati' and 'MC20' in mo) or
        # V10 Viper is collectible American exotic
        (m == 'Dodge' and 'Viper' in mo)
    )

    is_holder = (
        ('Land Cruiser' in mo or (m == 'Lexus' and 'LX' in mo) or
         (m == 'Toyota' and '4Runner' in mo) or
         (m == 'Lexus' and 'GX' in mo)) or
        (m == 'Toyota' and 'Supra' not in mo and 'Land Cruiser' not in mo and '4Runner' not in mo) or
        ('Civic Type R' in mo) or
        (m == 'Mazda' and 'MX-5' in mo)
    )

    is_fast_dep = (
        (body == 'SUV' and base >= 60000 and m in ('BMW', 'Audi', 'Mercedes-Benz')) or
        (m == 'Tesla' and yr >= 2018) or
        ('e-tron' in mo) or
        (m == 'Mercedes-Benz' and 'AMG' in mo and yr > 2015) or
        (m == 'Infiniti') or
        (m in ('Chrysler', 'VinFast', 'Hongqi', 'Polestar')) or
        # Italian brands depreciate heavily (Maserati worst, then Alfa Romeo, then Fiat)
        (m in ('Maserati', 'Alfa Romeo', 'Fiat')) or
        # Dodge V10 Viper is collectible - skip the fast-dep treatment
        (m == 'Dodge' and 'Viper' not in mo and 'Charger' not in mo and 'Challenger' not in mo)
    )

    is_holder = is_holder or (
        # Hellcats and Scat Packs hold value well (Mopar muscle)
        (m == 'Dodge' and ('Hellcat' in mo or 'Scat Pack' in mo or 'Demon' in mo)) or
        # Wrangler/Gladiator/TRX hold value
        (m == 'Jeep' and ('Wrangler' in mo or 'Gladiator' in mo or 'Trackhawk' in mo)) or
        # Ram TRX holds value
        (m == 'Ram' and 'TRX' in mo)
    )

    if is_icon:
        if yr < 1990:
            return int(base * 4.0)
        elif yr < 2000:
            return int(base * 2.5)
        elif yr < 2010:
            return int(base * 1.3)
        else:
            return int(base * 0.95)
    elif is_holder:
        if yr < 2010:
            return int(base * 0.85)
        elif yr < 2015:
            return int(base * 0.9)
        elif yr < 2018:
            return int(base * 0.92)
        elif yr < 2020:
            return int(base * 0.94)
        elif yr < 2022:
            return int(base * 0.96)
        else:
            return int(base * 0.98)
    elif is_fast_dep:
        if yr < 2020:
            return int(base * 0.55)
        else:
            return int(base * 0.65)
    else:
        if yr >= 2024:
            return int(base * 0.90)
        elif yr >= 2022:
            return int(base * 0.80)
        elif yr >= 2020:
            return int(base * 0.72)
        elif yr >= 2018:
            return int(base * 0.62)
        elif yr >= 2015:
            return int(base * 0.55)
        elif yr >= 2010:
            return int(base * 0.45)
        elif yr >= 2005:
            return int(base * 0.32)
        elif yr >= 2000:
            return int(base * 0.22)
        else:
            return int(base * 0.18)


def safe(v, fmt='.0f', default='--'):
    """Safe format that handles None."""
    if v is None:
        return default
    try:
        return format(v, fmt)
    except (ValueError, TypeError):
        return default


def main():
    conn = sqlite3.connect(str(ROOT / 'data' / 'motorgeek.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.year_start, c.make, c.model, c.variant, c.body_style, c.dougscore,
               pt.cargo_volume_liters,
               d.cargo_volume_liters_seats_down, d.seat_count,
               d.rear_legroom_mm, d.tow_capacity_kg, d.length_mm,
               b.q_score, r.reliability_score, z.zeperfs_index
        FROM cars c
        LEFT JOIN powertrain_ice pt ON pt.car_id = c.id
        LEFT JOIN dimensions d ON d.car_id = c.id
        LEFT JOIN build_quality b ON b.car_id = c.id
        LEFT JOIN reliability r ON r.car_id = c.id
        LEFT JOIN zeperfs_indices z ON z.car_id = c.id
    """)
    all_rows = cur.fetchall()

    cars = []
    for r in all_rows:
        car = Car()
        car.id = r['id']
        car.year_start = r['year_start']
        car.make = r['make']
        car.model = r['model']
        car.body_style = r['body_style']
        car.dougscore = r['dougscore']
        pt = PowertrainICE()
        pt.cargo_volume_liters = r['cargo_volume_liters']
        dim = Dimensions()
        dim.cargo_volume_liters_seats_down = r['cargo_volume_liters_seats_down']
        dim.seat_count = r['seat_count']
        dim.rear_legroom_mm = r['rear_legroom_mm']
        dim.tow_capacity_kg = r['tow_capacity_kg']
        p, _ = compute_practicality_for_car_v2(car, pt, None, dim)
        zp_norm = min(100.0, r['zeperfs_index'] / 3.0) if r['zeperfs_index'] else None
        v3 = compute_composite_v3(r['q_score'], r['reliability_score'], r['dougscore'], p, zp_norm)
        v2 = compute_composite(r['q_score'], r['reliability_score'], p, zp_norm)

        msrp = estimate_msrp({'make': r['make'], 'model': r['model'], 'year': r['year_start']})
        used = estimate_used_value({
            'make': r['make'], 'model': r['model'], 'year': r['year_start'],
            'body': r['body_style']
        })
        depreciation = (used - msrp) / msrp * 100 if msrp > 0 else 0

        cars.append({
            'id': r['id'], 'year': r['year_start'], 'make': r['make'],
            'model': r['model'], 'body': r['body_style'],
            'q': r['q_score'], 'r': r['reliability_score'], 'p': p,
            'z': zp_norm, 'd': r['dougscore'], 'v3': v3, 'v2': v2,
            'msrp': msrp, 'used': used,
            'change_pct': depreciation,
            'change_abs': used - msrp,
        })

    print("=" * 100)
    print("VALUE ANALYSIS -- new MSRP vs estimated current used price")
    print("=" * 100)
    print()

    print("=" * 100)
    print("TOP 15 APPRECIATING CARS (current value > new MSRP)")
    print("=" * 100)
    appreciating = [c for c in cars if c['change_abs'] > 0]
    appreciating.sort(key=lambda c: -c['change_abs'])
    header = "{:<6} {:<14} {:<22} {:>8} {:>8} {:>7} {:>5} {:<10}".format(
        "Year", "Make", "Model", "MSRP", "Now", "+/-", "v3", "body")
    print(header)
    print("-" * 100)
    for c in appreciating[:15]:
        line = "{:<6} {:<14} {:<22} ${:>5.0f}K ${:>5.0f}K {:>+5.0f}% {:>5} {:<10}".format(
            c['year'], c['make'], c['model'], c['msrp']/1000, c['used']/1000,
            c['change_pct'], safe(c['v3']), c['body'] or "--")
        print(line)

    print()
    print("=" * 100)
    print("TOP 15 FASTEST-DEPRECIATING CARS (current value << new MSRP)")
    print("=" * 100)
    depreciating = [c for c in cars if c['change_abs'] < 0]
    depreciating.sort(key=lambda c: c['change_abs'])
    print(header)
    print("-" * 100)
    for c in depreciating[:15]:
        line = "{:<6} {:<14} {:<22} ${:>5.0f}K ${:>5.0f}K {:>+5.0f}% {:>5} {:<10}".format(
            c['year'], c['make'], c['model'], c['msrp']/1000, c['used']/1000,
            c['change_pct'], safe(c['v3']), c['body'] or "--")
        print(line)

    print()
    print("=" * 100)
    print("BEST VALUE PER V3 POINT -- lowest $/v3 ratio")
    print("=" * 100)
    valued = [c for c in cars if c['v3'] is not None and c['used'] > 5000]
    valued.sort(key=lambda c: c['used'] / c['v3'])
    header2 = "{:<6} {:<14} {:<22} {:>8} {:>5} {:>9} {:<10}".format(
        "Year", "Make", "Model", "Used", "v3", "$/v3", "body")
    print(header2)
    print("-" * 90)
    for c in valued[:15]:
        ratio = c['used'] / c['v3'] / 1000
        line = "{:<6} {:<14} {:<22} ${:>5.0f}K {:>5.1f} ${:>6.1f}K {:<10}".format(
            c['year'], c['make'], c['model'], c['used']/1000, c['v3'], ratio, c['body'] or "--")
        print(line)

    print()
    print("=" * 100)
    print("DEPRECIATION BY BODY STYLE (avg % change)")
    print("=" * 100)
    bodies = {}
    for c in cars:
        bodies.setdefault(c['body'] or 'unknown', []).append(c)
    print("{:<14} {:>4} {:>10} {:>10} {:>11} {:>8}".format(
        "Body", "n", "avg MSRP", "avg Used", "avg delta", "avg %"))
    print("-" * 70)
    for body, lst in sorted(bodies.items(), key=lambda x: -len(x[1])):
        if not lst:
            continue
        avg_msrp = sum(c['msrp'] for c in lst) / len(lst)
        avg_used = sum(c['used'] for c in lst) / len(lst)
        avg_delta = avg_used - avg_msrp
        avg_pct = avg_delta / avg_msrp * 100 if avg_msrp > 0 else 0
        print("{:<14} {:>4} ${:>6.0f}K ${:>6.0f}K ${:>+7.1f}K {:>+6.1f}%".format(
            body, len(lst), avg_msrp/1000, avg_used/1000, avg_delta/1000, avg_pct))

    print()
    print("=" * 100)
    print("DEPRECIATION BY MAKE (avg % change)")
    print("=" * 100)
    makes = {}
    for c in cars:
        makes.setdefault(c['make'], []).append(c)
    print("{:<14} {:>4} {:>8} {:<22} {:<22}".format(
        "Make", "n", "avg %", "best hold", "worst drop"))
    print("-" * 80)
    for make, lst in sorted(makes.items(), key=lambda x: -sum(c['change_pct'] for c in x[1]) / len(x[1])):
        if not lst:
            continue
        avg_pct = sum(c['change_pct'] for c in lst) / len(lst)
        best = max(lst, key=lambda c: c['change_pct'])
        worst = min(lst, key=lambda c: c['change_pct'])
        print("{:<14} {:>4} {:>+6.1f}%  {:<4} {:<16} {:<4} {:<16}".format(
            make, len(lst), avg_pct,
            best['year'], (best['model'] or '--')[:16],
            worst['year'], (worst['model'] or '--')[:16]))

    conn.close()


if __name__ == "__main__":
    main()
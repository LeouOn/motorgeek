"""Build a BUDGET dream garage -- realistic aspirational picks, not unobtainium.

Filters by approximate new MSRP bands:
  - <$35K:   entry luxury / sport compact
  - $35-55K: mainstream luxury (3-series, C-class, etc.)
  - $55-80K: premium luxury (5-series, E-class, etc.)
  - $80-120K: high luxury (M3, AMG, RS, etc.)
  - $120K+:  unobtainium (LX, G-Wagon, AMG GT, etc.)

The brief: show 3-5 cars in each band that score best on v3 composite,
so the user can see "what's actually achievable at each price point".
"""
import sqlite3
import sys
from pathlib import Path

ROOT = Path('C:/Users/llama/OneDrive/proj/motorgeek')
sys.path.insert(0, str(ROOT))

from motorgeek.core.calculators.composite import compute_composite, compute_composite_v3
from motorgeek.core.calculators.practicality import compute_practicality_for_car_v2
from motorgeek.core.models import Car, Dimensions, PowertrainICE


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
        cars.append({
            'id': r['id'], 'year': r['year_start'], 'make': r['make'],
            'model': r['model'], 'variant': r['variant'] or '',
            'body': r['body_style'],
            'q': r['q_score'], 'r': r['reliability_score'], 'p': p,
            'z_raw': r['zeperfs_index'], 'z': zp_norm,
            'd': r['dougscore'],
            'v3': v3, 'v2': v2,
            'length_mm': r['length_mm'],
        })

    def fmt(v):
        return f"{v:.0f}" if v is not None else "--"

    # APPROXIMATE new-MSRP bands (USD).
    # These are rough estimates based on typical trim levels for each model/year.
    # Order: (lo, hi, label)
    bands = [
        ("<$35K (entry luxury / sport compact)", 0, 35000),
        ("$35-55K (mainstream luxury)",          35000, 55000),
        ("$55-80K (premium luxury)",             55000, 80000),
        ("$80-120K (high luxury)",               80000, 120000),
        ("$120K+ (unobtainium)",                 120000, 999999),
    ]

    # Rough MSRP estimates for each model.
    # Using approximate new-car MSRP for the trim level we have in DB.
    # Years matter: 2020+ cars are close to new MSRP, older are inflation-adjusted estimates.
    def estimate_msrp(c):
        """Return approximate new MSRP in USD for this car."""
        m, mo, yr = c['make'], c['model'], c['year']
        # Performance / AMG / M / RS / Blackwing / Turbo GT etc.
        is_perf = any(x in mo for x in ('AMG', 'M3', 'M4', 'M5', 'M6', 'M8',
                                         'RS', 'Turbo GT', 'Turbo S', 'Blackwing',
                                         'GT-R', 'Type R', 'Hellcat', 'GT350',
                                         'GT500', 'Shelby', 'SS', 'ZL1', 'Z06',
                                         'Turbo', 'GT3', 'GT', 'Plaid', 'Nismo',
                                         'CT5-V', 'CT4-V', 'AMG', 'Maybach',
                                         'Cayman', 'Supra', 'NSX', 'i8'))
        is_luxury_suv = any(x in mo for x in ('LX', 'GX', 'LX570', 'LX 600', 'Navigator',
                                              'Escalade', 'LX 600', 'Aviator', 'GLS',
                                              'GLE', 'GLC', 'X5', 'X6', 'X7', 'Q7', 'Q8',
                                              'RSQ8', 'Bentayga', 'Cullinan', 'Urus',
                                              'Levante', 'Defender', 'Range Rover',
                                              'Cayenne', 'Macan', 'Panamera'))
        # Per-model base MSRP estimates (2020-era)
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
        elif m == 'Honda':
            base = 28000
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
        elif m == 'Polestar':
            base = 50000
        elif m == 'Fiat':
            base = 30000
        elif m == 'BYD':
            base = 40000
        elif m == 'Xiaomi':
            base = 30000
        else:
            base = 35000

        # Adjust for older years (pre-2015 get a discount on "new" MSRP)
        if yr < 2010:
            return int(base * 0.6)
        elif yr < 2015:
            return int(base * 0.75)
        elif yr < 2018:
            return int(base * 0.85)
        elif yr < 2020:
            return int(base * 0.92)
        elif yr < 2022:
            return int(base * 0.98)
        else:
            return int(base * 1.0)

    for car in cars:
        car['msrp'] = estimate_msrp(car)

    print("=" * 100)
    print("REALISTIC DREAM GARAGE -- top v3 cars in each MSRP band")
    print("=" * 100)
    print()

    for label, lo, hi in bands:
        band_cars = [c for c in cars if lo <= c['msrp'] < hi and c['v3'] is not None]
        band_cars.sort(key=lambda c: -c['v3'])
        if not band_cars:
            print(f"### {label}")
            print("   (no v3-rankable cars in this band)")
            print()
            continue
        print(f"### {label}")
        print(f"   {len(band_cars)} cars qualify. Top 5:")
        for c in band_cars[:5]:
            v3_str = f"v3={c['v3']:.1f}"
            d_str = f" D={c['d']}" if c['d'] else " D=--"
            msrp_str = f"~${c['msrp']/1000:.0f}K"
            len_str = f"  {c['length_mm']:.0f}mm" if c['length_mm'] else ""
            print(f"      {c['year']} {c['make']} {c['model']:<25} {v3_str}{d_str}  Q={fmt(c['q'])} R={fmt(c['r'])} P={fmt(c['p'])} Z={fmt(c['z'])}  {msrp_str}{len_str}")
        print()

    # Show a specific realistic aspirational lineup
    print("=" * 100)
    print("REALISTIC ASPIRATIONAL LINEUP -- one car per band, the best v3 in each")
    print("=" * 100)
    print()
    for label, lo, hi in bands:
        band_cars = [c for c in cars if lo <= c['msrp'] < hi and c['v3'] is not None]
        if not band_cars:
            continue
        best = max(band_cars, key=lambda c: c['v3'])
        v3_str = f"v3={best['v3']:.1f}"
        d_str = f" D={best['d']}" if best['d'] else " D=--"
        msrp_str = f"~${best['msrp']/1000:.0f}K"
        print(f"   {label}")
        print(f"      -> {best['year']} {best['make']} {best['model']} {v3_str}{d_str}  Q={fmt(best['q'])} R={fmt(best['r'])} P={fmt(best['p'])} Z={fmt(best['z'])}  {msrp_str}")
    print()

    # Cross-band dream: 3 cars total under $80K total
    print("=" * 100)
    print("UNDER $80K TOTAL -- best possible 3-car lineup (daily + fun + SUV)")
    print("=" * 100)
    print()

    # Find best daily sedan, best fun car, best SUV, each under $40K
    # Use 'best' to mean highest v3 per category within the sub-budget
    print("Strategy: 3 cars, ~$25K each (or unbalanced: 1 expensive + 2 cheap)")
    print()
    candidates_sedan = [c for c in cars if c['body'] == 'sedan' and c['v3'] is not None and c['msrp'] <= 40000]
    candidates_coupe = [c for c in cars if c['body'] == 'coupe' and c['v3'] is not None and c['msrp'] <= 50000]
    candidates_suv = [c for c in cars if c['body'] == 'SUV' and c['v3'] is not None and c['msrp'] <= 50000]

    candidates_sedan.sort(key=lambda c: -c['v3'])
    candidates_coupe.sort(key=lambda c: -c['v3'])
    candidates_suv.sort(key=lambda c: -c['v3'])

    for label, lst in [("Daily sedan (under $40K)", candidates_sedan[:3]),
                       ("Fun car / coupe (under $50K)", candidates_coupe[:3]),
                       ("Compact SUV (under $50K)", candidates_suv[:3])]:
        print(f"### {label}")
        for c in lst:
            v3_str = f"v3={c['v3']:.1f}"
            d_str = f" D={c['d']}" if c['d'] else " D=--"
            msrp_str = f"~${c['msrp']/1000:.0f}K"
            print(f"   {c['year']} {c['make']} {c['model']:<25} {v3_str}{d_str}  Q={fmt(c['q'])} R={fmt(c['r'])} P={fmt(c['p'])} Z={fmt(c['z'])}  {msrp_str}")
        print()

    conn.close()


if __name__ == "__main__":
    main()
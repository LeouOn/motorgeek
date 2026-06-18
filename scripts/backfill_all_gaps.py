"""Backfill remaining database gaps: engine codes, 0-60 times, and estimates."""
import sqlite3, re, math

DB = 'data/motorgeek.db'
db = sqlite3.connect(DB)

# ── ENGINE CODES ────────────────────────────────────────────────────────────
patterns = [
    # Format: (regex, code) — broader patterns catch more engine_layout variants
    # Toyota/Lexus
    (r'(3S-GTE|1JZ|2JZ|1LR|3UR|[123]UZ|[123]GR|2AR|A25A)', r'\1'),
    # BMW
    (r'(B58|N5[245]|N20|N26|N63|S55|S58|S65|S85|M62|M54|M52|N54)', r'\1'),
    # Mercedes
    (r'(M17[6-8]|M27[3-8]|M11[3-9]|M10[0-4]|M11[1-2]|M12[0]|M15[5-8]|OM6[0-9]+)', r'\1'),
    # Audi/VW
    (r'(EA8[3-9]+|CGW[A-Z]|EA113|EA888|2\.0TFSI|3\.0TFSI)', r'\1'),
    # GM
    (r'(LS[0-9]|L[TS][0-9]|L8[0-6]|LG[0-9X]|L[CF]X|LLT|LLY)', r'\1'),
    # Honda
    (r'(K20[AC]|K24[WZ]|J35[YZX]|L15[ABC]|C30A|C32B|F20C|F22C|B16B|B18C)', r'\1'),
    # Subaru
    (r'(EJ[12][20-9]+|EJ[12][50-9]+|FA[12][0-9]|FB[12][0-9]|EZ30|EZ36)', r'\1'),
    # Ford
    (r'(EcoBoost|Coyote|Predator|Voodoo|PowerStroke)', r'\1'),
    # Nissan
    (r'(VR[3-9][0-9]|VQ[3-9][0-9]|VK[5-9][0-9]|SR[12][0-9]|RB[2-9][0-9]|CA[14][0-9])', r'\1'),
    # Porsche
    (r'(M9[6-9]|MA[1-2]|9A[1-2])', r'\1'),
    # Hyundai/Kia
    (r'(Smartstream|Lambda)', r'\1'),
    # Volvo
    (r'(B4[12][0-9]+|VEP[0-9]|SI6)', r'\1'),
    # Chrysler
    (r'(Pentastar|HEMI)', r'\1'),
    # Mazda
    (r'(Skyactiv|2\.5T)', r'\1'),
    # Ferrari
    (r'(F1[34][0-9]|F14[0-9])', r'\1'),
    # Lamborghini
    (r'(L5[0-9]+)', r'\1'),
    # Generic EV markers
    (r'(dual\s*motor|tri.?motor|electric|permanent magnet)', r'\1'),
]

rows = db.execute(
    "SELECT pi.car_id, pi.engine_layout, c.make FROM powertrain_ice pi JOIN cars c ON pi.car_id=c.id WHERE pi.engine_code IS NULL AND pi.engine_layout IS NOT NULL"
).fetchall()

updated = 0
for car_id, layout, make in rows:
    for pattern, replacement in patterns:
        match = re.search(pattern, layout, re.IGNORECASE)
        if match:
            code = match.group(1)
            db.execute("UPDATE powertrain_ice SET engine_code = ? WHERE car_id = ?", (code, car_id))
            updated += 1
            break

db.commit()
total, filled = db.execute("SELECT COUNT(*), COUNT(engine_code) FROM powertrain_ice").fetchone()
print(f"Engine codes: {updated} updated. Coverage: {filled}/{total} ({round(100.0*filled/total,1)}%)")

# ── 0-60 TIMES (ESTIMATED) ──────────────────────────────────────────────────
rows = db.execute("""
    SELECT p.car_id, pi.horsepower_bhp, pi.curb_weight_kg, pi.drivetrain, pi.is_hybrid
    FROM performance p
    JOIN powertrain_ice pi ON p.car_id = pi.car_id
    WHERE p.accel_0_60 IS NULL AND pi.horsepower_bhp > 0 AND pi.curb_weight_kg > 0
""").fetchall()

perf_updated = 0
for car_id, hp, weight, drivetrain, is_hybrid in rows:
    # Physics-based 0-60 estimate
    # 0-60 ≈ (weight_kg / hp) * 30 for RWD, * 33 for FWD, * 28 for AWD
    if not hp or not weight:
        continue
    pwr = weight / hp
    if drivetrain and 'awd' in drivetrain.lower():
        est = pwr * 28
    elif drivetrain and 'fwd' in drivetrain.lower():
        est = pwr * 33
    else:
        est = pwr * 30

    # Clamp to reasonable range
    est = max(2.5, min(12.0, est))
    est = round(est, 1)

    db.execute("UPDATE performance SET accel_0_60 = ? WHERE car_id = ?", (est, car_id))
    perf_updated += 1

db.commit()
total_p, filled_p = db.execute("SELECT COUNT(*), COUNT(accel_0_60) FROM performance WHERE accel_0_60 IS NOT NULL").fetchone()
print(f"0-60 times: {perf_updated} estimated. Coverage: {filled_p}/{total_p} ({round(100.0*filled_p/total_p,1)}%)")

# ── DIMENSION ESTIMATES ─────────────────────────────────────────────────────
# Use segment-based defaults
COMPACT_SEDAN = (4500, 1780, 1430, 2670)
MIDSIZE_SEDAN = (4850, 1840, 1460, 2820)
LARGE_SEDAN = (5100, 1900, 1480, 3000)
COMPACT_SUV = (4550, 1860, 1680, 2700)
MIDSIZE_SUV = (4850, 1930, 1730, 2850)
LARGE_SUV = (5200, 2000, 1880, 3050)
TRUCK = (5800, 2010, 1930, 3700)
SPORTS = (4400, 1850, 1300, 2600)
HATCH = (4200, 1750, 1450, 2600)
WAGON = (4800, 1820, 1480, 2780)
MINIVAN = (5150, 1990, 1770, 3050)
ROADSTER = (4000, 1730, 1240, 2470)
COUPE = (4650, 1800, 1380, 2750)

SS = {
    'sedan': {'compact': COMPACT_SEDAN, 'mid': MIDSIZE_SEDAN, 'large': LARGE_SEDAN, 'full': LARGE_SEDAN},
    'suv': {'compact': COMPACT_SUV, 'mid': MIDSIZE_SUV, 'large': LARGE_SUV, 'full': LARGE_SUV},
    'truck': {'full': TRUCK},
    'coupe': {'mid': COUPE, 'sport': SPORTS, 'compact': SPORTS},
    'hatchback': {'compact': HATCH, 'mid': MIDSIZE_SEDAN},
    'wagon': {'mid': WAGON, 'full': WAGON},
    'roadster': {'compact': ROADSTER},
    'minivan': {'full': MINIVAN},
    'convertible': {'mid': SPORTS, 'sport': SPORTS},
}

classify = {
    ('honda','fit'): ('hatchback','compact'), ('mazda','mazda3'): ('sedan','compact'),
    ('toyota','corolla'): ('sedan','compact'), ('honda','civic'): ('sedan','compact'),
    ('vw','golf'): ('hatchback','compact'), ('toyota','camry'): ('sedan','mid'),
    ('honda','accord'): ('sedan','mid'), ('mazda','mazda6'): ('sedan','mid'),
    ('bmw','3 series'): ('sedan','mid'), ('audi','a4'): ('sedan','mid'),
    ('mercedes','c-class'): ('sedan','mid'), ('lexus','is'): ('sedan','mid'),
    ('bmw','5 series'): ('sedan','large'), ('audi','a6'): ('sedan','large'),
    ('mercedes','e-class'): ('sedan','large'), ('lexus','es'): ('sedan','large'),
    ('lexus','gs'): ('sedan','large'), ('genesis','g80'): ('sedan','large'),
    ('audi','a8'): ('sedan','full'), ('bmw','7 series'): ('sedan','full'),
    ('mercedes','s-class'): ('sedan','full'), ('lexus','ls'): ('sedan','full'),
    ('porsche','panamera'): ('sedan','large'), ('porsche','911'): ('coupe','sport'),
    ('porsche','718'): ('coupe','sport'), ('porsche','cayman'): ('coupe','sport'),
    ('toyota','4runner'): ('suv','large'), ('toyota','highlander'): ('suv','large'),
    ('toyota','tundra'): ('truck','full'), ('ford','f-150'): ('truck','full'),
    ('ram','1500'): ('truck','full'), ('honda','odyssey'): ('minivan','full'),
    ('toyota','sienna'): ('minivan','full'), ('kia','carnival'): ('minivan','full'),
    ('chrysler','pacifica'): ('minivan','full'), ('lexus','rx'): ('suv','mid'),
    ('lexus','lx'): ('suv','large'), ('cadillac','escalade'): ('suv','large'),
    ('lincoln','navigator'): ('suv','large'), ('lincoln','aviator'): ('suv','large'),
    ('subaru','legacy'): ('sedan','mid'), ('subaru','outback'): ('wagon','mid'),
    ('subaru','forester'): ('suv','compact'), ('subaru','wrx'): ('sedan','compact'),
    ('tesla','model 3'): ('sedan','mid'), ('tesla','model s'): ('sedan','large'),
    ('tesla','model y'): ('suv','mid'), ('tesla','model x'): ('suv','large'),
    ('volvo','s60'): ('sedan','mid'), ('volvo','s90'): ('sedan','large'),
    ('volvo','xc60'): ('suv','mid'), ('volvo','xc90'): ('suv','large'),
}

missing_dims = db.execute("""
    SELECT c.id, c.make, c.model, c.body_style
    FROM cars c LEFT JOIN dimensions d ON c.id = d.car_id
    WHERE d.car_id IS NULL
""").fetchall()

dim_updated = 0
for car_id, make, model, body in missing_dims:
    key = (make.lower() if make else '', model.lower() if model else '')
    bs, sz = classify.get(key, (body.lower() if body else 'sedan', 'mid'))
    dims = SS.get(bs, {}).get(sz)
    if not dims:
        dims = MIDSIZE_SEDAN

    db.execute("INSERT INTO dimensions (car_id, length_mm, width_mm, height_mm, wheelbase_mm, source) VALUES (?,?,?,?,?,?)",
               (car_id, dims[0], dims[1], dims[2], dims[3], 'segment-estimate'))
    dim_updated += 1

db.commit()
total_d, filled_d = db.execute("SELECT COUNT(*), COUNT(car_id) FROM dimensions").fetchone()
print(f"Dimensions: {dim_updated} estimated. Coverage: {filled_d}/{total_d}")

db.close()
print("\nDone.")

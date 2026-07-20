"""Compute ZePerfs ZP scores and validate against known values."""
import sqlite3, math

DB = "data/motorgeek.db"

# v4 ICE formula (refit on 22 anchors, MAE 2.99)
def zp_ice(hp, weight_kg, disp_cc, accel_0_60):
    """Compute ZP for ICE cars using v4 formula."""
    if not hp or not weight_kg or not disp_cc or not accel_0_60:
        return None
    ch_T = hp / (weight_kg / 1000.0)  # power per tonne
    ch_L = hp / (disp_cc / 1000.0)     # specific output (hp/L)
    tpu = 10.0 / accel_0_60            # accel inverse (0-100 km/h)
    
    zp = (0.3924 * ch_T 
          - 0.4383 * math.sqrt(ch_L) 
          + 56.1399 * tpu 
          - 10.4664 * (ch_T * tpu / 100.0) 
          + 13.3050)
    return round(zp, 1)

# EV formula v3
def zp_ev(hp, weight_kg, accel_0_60):
    """Compute ZP for EV cars using v3 log(chT) formula."""
    if not hp or not weight_kg or not accel_0_60:
        return None
    ch_T = hp / (weight_kg / 1000.0)
    tpu = 10.0 / accel_0_60
    
    zp = 55.48 * math.log(ch_T) + 12.28 * tpu - 162.24
    return round(zp, 1)

db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

# Get all cars with known zeperfs values AND powertrain data
rows = db.execute("""
    SELECT c.id, c.make, c.model, c.variant,
           pi.horsepower_bhp, pi.curb_weight_kg, pi.displacement_cc,
           pi.is_hybrid, pi.engine_layout,
           p.accel_0_60,
           z.zeperfs_index AS known_zp
    FROM cars c
    JOIN zeperfs_indices z ON c.id = z.car_id
    LEFT JOIN powertrain_ice pi ON c.id = pi.car_id
    LEFT JOIN performance p ON c.id = p.car_id
    WHERE z.zeperfs_index IS NOT NULL
      AND pi.horsepower_bhp IS NOT NULL
      AND pi.curb_weight_kg IS NOT NULL
      AND p.accel_0_60 IS NOT NULL
    ORDER BY z.zeperfs_index DESC
""").fetchall()

print("=" * 90)
print(f"{'Car':<40} {'Known':>6} {'Calc':>6} {'Error':>6} {'HP':>5} {'Wt':>5} {'0-60':>5} {'ch/T':>6}")
print("=" * 90)

errors = []
for r in rows:
    known = r['known_zp']
    hp = r['horsepower_bhp']
    wt = r['curb_weight_kg']
    disp = r['displacement_cc'] or 0
    accel = r['accel_0_60']
    
    # Determine if EV
    layout = (r['engine_layout'] or '').lower()
    is_ev = ('electric' in layout or 'motor' in layout or 'dual motor' in layout 
             or 'tri-motor' in layout or disp == 0 or disp < 500)
    
    if is_ev and disp == 0:
        calc = zp_ev(hp, wt, accel)
        formula = "EV"
    elif disp > 0:
        calc = zp_ice(hp, wt, disp, accel)
        formula = "ICE"
    else:
        calc = None
        formula = "?"
    
    if calc and known:
        err = calc - known
        errors.append(abs(err))
        ch_T = hp / (wt / 1000.0)
        name = f"{r['make']} {r['model']} {r['variant'] or ''}"[:38]
        marker = " ***" if abs(err) > 15 else ""
        print(f"{name:<40} {known:>6.1f} {calc:>6.1f} {err:>+6.1f} {hp:>5.0f} {wt:>5.0f} {accel:>5.1f} {ch_T:>6.1f}{marker}")
    elif calc:
        print(f"{r['make']} {r['model']:<20} {'?':>6} {calc:>6.1f} {'?':>6} {hp:>5.0f} {wt:>5.0f} {accel:>5.1f}")

print("=" * 90)
if errors:
    mae = sum(errors) / len(errors)
    max_err = max(errors)
    print(f"\nMAE: {mae:.1f} | Max error: {max_err:.1f} | Samples: {len(errors)}")
    
    # Error distribution
    under5 = sum(1 for e in errors if e < 5)
    under10 = sum(1 for e in errors if e < 10)
    under15 = sum(1 for e in errors if e < 15)
    over15 = sum(1 for e in errors if e >= 15)
    print(f"Within  5 pts: {under5}/{len(errors)} ({100*under5/len(errors):.0f}%)")
    print(f"Within 10 pts: {under10}/{len(errors)} ({100*under10/len(errors):.0f}%)")
    print(f"Within 15 pts: {under15}/{len(errors)} ({100*under15/len(errors):.0f}%)")
    print(f"Over 15 pts:   {over15}/{len(errors)} ({100*over15/len(errors):.0f}%)")
else:
    print("\nNo comparable data.")

# Now compute ZP for the specific cars user asked about
print("\n" + "=" * 90)
print("USER-REQUESTED COMPARISON CARS")
print("=" * 90)

target_cars = db.execute("""
    SELECT c.id, c.make, c.model, c.variant,
           pi.horsepower_bhp, pi.curb_weight_kg, pi.displacement_cc,
           pi.engine_layout, pi.drivetrain,
           p.accel_0_60,
           z.zeperfs_index AS known_zp,
           r.reliability_score,
           b.q_score,
           b.score_body_construction, b.score_nvh_isolation, b.score_chassis
    FROM cars c
    LEFT JOIN powertrain_ice pi ON c.id = pi.car_id
    LEFT JOIN performance p ON c.id = p.car_id
    LEFT JOIN zeperfs_indices z ON c.id = z.car_id
    LEFT JOIN reliability r ON c.id = r.car_id
    LEFT JOIN build_quality b ON c.id = b.car_id
    WHERE (LOWER(c.model) LIKE '%mazda6%' OR LOWER(c.model) LIKE '%mazda3%'
       OR LOWER(c.model) LIKE '%a4%' OR LOWER(c.model) LIKE '%a6%'
       OR (LOWER(c.model) = '3 series' AND c.variant LIKE '%320%')
       OR (LOWER(c.make) = 'bmw' AND LOWER(c.variant) LIKE '%320%')
       OR (LOWER(c.make) = 'bmw' AND LOWER(c.model) LIKE '%3 series%')
       OR (LOWER(c.make) = 'bmw' AND LOWER(c.variant) LIKE '%328%')
       OR (LOWER(c.make) = 'audi' AND (LOWER(c.model) LIKE '%a4%'))
       OR (LOWER(c.make) = 'mercedes' AND LOWER(c.model) = 'c-class'
           AND (LOWER(c.variant) LIKE '%c300%' OR LOWER(c.variant) LIKE '%c200%')))
    ORDER BY c.make, c.model
""").fetchall()

print(f"\n{'Car':<45} {'Known':>6} {'Calc':>6} {'Rel':>5} {'Q':>5} {'HP':>5} {'Wt':>5} {'0-60':>5} {'Drv':>8}")
print("-" * 90)

for r in target_cars:
    hp = r['horsepower_bhp'] or 0
    wt = r['curb_weight_kg'] or 0
    disp = r['displacement_cc'] or 0
    accel = r['accel_0_60'] or 0
    known = r['known_zp']
    
    layout = (r['engine_layout'] or '').lower()
    is_ev = disp < 500
    
    if hp and wt and accel:
        if is_ev:
            calc = zp_ev(hp, wt, accel)
        elif disp > 0:
            calc = zp_ice(hp, wt, disp, accel)
        else:
            calc = None
    else:
        calc = None
    
    name = f"{r['make']} {r['model']} {r['variant'] or ''}"[:43]
    k = f"{known:.1f}" if known else "?"
    c = f"{calc:.1f}" if calc else "?"
    rel = f"{r['reliability_score']:.0f}" if r['reliability_score'] else "?"
    q = f"{r['q_score']:.0f}" if r['q_score'] else "?"
    drv = r['drivetrain'] or "?"
    print(f"{name:<45} {k:>6} {c:>6} {rel:>5} {q:>5} {hp:>5.0f} {wt:>5.0f} {accel:>5.1f} {drv:>8}")

db.close()

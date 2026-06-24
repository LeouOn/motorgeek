"""MotorGeek 5-Way ranking: Rel + Q + Cap + Mod + Value + Maint.
Reads from the cleaned motorgeek.db."""
import sqlite3, math, json

DB = 'data/motorgeek.db'

def load():
    db = sqlite3.connect(DB)
    cur = db.cursor()
    cur.execute('''
    SELECT c.id, c.make, c.model, c.generation, c.year_start, c.year_end,
           c.body_style, c.country, c.family, c.variant, c.character, c.era_tag,
           p.cargo_volume_liters, p.curb_weight_kg, p.ground_clearance_mm,
           p.horsepower_bhp, p.displacement_cc, p.aspiration, p.is_hybrid,
           p.fuel_consumption_mixed_l_100km,
           d.length_mm, d.width_mm, d.height_mm, d.wheelbase_mm,
           r.reliability_score, r.score_engine, r.score_transmission,
           r.score_chassis, r.score_electronics, r.score_ease_of_repair,
           r.part_availability, r.diy_friendliness,
           bq.q_score,
           mh.price_low, mh.price_high
    FROM cars c
    LEFT JOIN powertrain_ice p ON c.id = p.car_id
    LEFT JOIN dimensions d ON c.id = d.car_id
    LEFT JOIN reliability r ON c.id = r.car_id
    LEFT JOIN build_quality bq ON c.id = bq.car_id
    LEFT JOIN market_history mh ON mh.id = (
        SELECT mh2.id FROM market_history mh2
        WHERE mh2.car_id = c.id
        ORDER BY mh2.date_recorded DESC
        LIMIT 1
    )
    ORDER BY c.id
    ''')
    cars = [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]
    db.close()
    return cars


# ── Normalizers ────────────────────────────────────────────────────────────

def norm_parts(text):
    if not text: return None
    t = text.lower().strip()
    if 'excellent' in t or 'massive' in t or 'everywhere' in t: return 95
    if t.startswith('good') or 'good (' in t or 'good ' in t or t == 'good': return 75
    if 'abundant' in t or 'plentiful' in t or 'tons' in t: return 80
    if 'moderate' in t or 'fair' in t: return 50
    if 'limited' in t: return 30
    if 'poor' in t or 'scarce' in t or 'very poor' in t or 'nonexistent' in t: return 15
    if 'specialist' in t: return 35
    if 'dealer' in t: return 40
    return 50

def norm_diy(text):
    if not text: return None
    t = text.lower().strip()
    if 'very_high' in t or 'very high' in t: return 95
    if t.startswith('high') or 'simple' in t or 'every mechanic' in t: return 85
    if t == 'high': return 85
    if 'good' in t: return 75
    if 'moderate' in t or t == 'moderate': return 50
    if 'difficult' in t or t == 'low' or t.startswith('low'): return 25
    if 'very_low' in t or 'very low' in t: return 10
    if 'specialist' in t or 'dealer' in t: return 20
    return 50

# ── Tables ─────────────────────────────────────────────────────────────────

KNOWN_ASP = {41: 'twin-turbo'}
def infer_asp(c):
    if c['id'] in KNOWN_ASP: return KNOWN_ASP[c['id']]
    if c['asp'] and c['asp'] != '?': return c['asp']
    if c['cc'] is None and c['hp']: return 'electric'
    if c['char'] == 'ev': return 'electric'
    if c['hybrid']:
        if c['cc'] and c['hp'] and c['cc'] > 0:
            hpl = c['hp']/(c['cc']/1000)
            return 'turbocharged + e-motor' if hpl > 100 else 'naturally aspirated + e-motor'
        return 'turbocharged + e-motor'
    if c['cc'] and c['hp'] and c['cc'] > 0:
        hpl = c['hp'] / (c['cc']/1000)
        if hpl > 150: return 'twin-turbo'
        if hpl > 100: return 'turbocharged'
        return 'naturally aspirated'
    if c['cc'] and c['cc'] > 5000: return 'naturally aspirated'
    return 'naturally aspirated'

ASP_SCORE = {
    'electric': 0, 'electric (dual motor)': 0,
    'naturally aspirated': 30, 'Naturally aspirated': 30, 'natural': 30,
    'naturally aspirated VTEC': 35, 'naturally aspirated flat-plane-crank': 40,
    'naturally aspirated rotary': 25, 'naturally aspirated + e-motor': 15,
    'turbo': 75, 'Turbocharged': 75, 'turbocharged': 75,
    'Single turbo': 75, 'single turbo': 75, 'turbocharged VTEC': 80,
    'turbocharged flat-4': 80, 'turbocharged + e-motor': 65,
    'turbocharged + intercooler': 80, 'Single turbo (BorgWarner)': 80,
    'Single twin-scroll turbo (hot-vee)': 80,
    'Twin-turbo': 90, 'twin-turbo': 90, 'BiTurbo': 90, 'BiTurbo (hot-vee)': 90,
    'twin-turbo V6': 90, 'twin-turbo rotary': 85, 'twin-turbocharged': 90,
    'Twin-turbo (hot-V) + 48V EQ Boost': 80,
    'supercharged': 70, 'Supercharged (Eaton TVS)': 75,
    'Supercharged (Lysholm screw-type, 11.6 psi)': 80,
    'Turbo + Eaton Roots supercharger': 95, 'twin-charged (supercharger+turbo)': 95,
}
COUNTRY_AM = {'Japan': 95, 'Germany': 85, 'USA': 80, 'USA/Canada': 80,
    'South Korea': 45, 'Sweden': 45, 'United Kingdom': 55,
    'Italy': 50, 'France': 40, 'China': 30, 'Vietnam': 15,
    'Australia': 50, 'Japan/USA': 90, 'Japan/Canada': 90, 'Japan/Mexico': 85}
CHAR_MOD = {'hot': 1.0, 'hyper': 1.0, 'muscle': 1.0, 'sleeper': 0.90, 'sport': 0.85,
    'warm': 0.70, 'classic': 0.60,
    'eco': 0.15, 'ev': 0.0, 'commuter': 0.20,
    'family': 0.25, 'utility': 0.20,
    'luxury': 0.20, 'executive': 0.20, 'premium': 0.25,
    'adventure': 0.50, 'performance-suv': 0.60,
    'refined': 0.30, 'understated': 0.30, 'versatile': 0.30, 'practical': 0.20, 'sharp': 0.40}
BODY_CAP = {'minivan': 95, 'truck': 90, 'SUV': 85, 'wagon': 80,
    'hatchback': 55, 'liftback': 55, 'sedan': 50, 'four-door coupe': 40,
    'coupe': 25, 'roadster': 10, None: 40}

# ── Helpers ────────────────────────────────────────────────────────────────

def pct(val, lst):
    if val is None or not lst: return None
    return round(sum(1 for v in lst if v <= val) / len(lst) * 100, 1)

# ── Main ───────────────────────────────────────────────────────────────────

def rank():
    raw = load()
    C = []
    for r in raw:
        C.append({
            'id': r['id'], 'make': r['make'], 'model': r['model'], 'gen': r['generation'],
            'year': r['year_start'], 'body': r['body_style'], 'country': r['country'],
            'family': r['family'], 'variant': r['variant'], 'char': r['character'],
            'cargo_l': r['cargo_volume_liters'], 'wt': r['curb_weight_kg'],
            'gc': r['ground_clearance_mm'], 'hp': r['horsepower_bhp'],
            'cc': r['displacement_cc'], 'asp': r['aspiration'],
            'hybrid': r['is_hybrid'], 'fuel': r['fuel_consumption_mixed_l_100km'],
            'len': r['length_mm'], 'wid': r['width_mm'],
            'hgt': r['height_mm'], 'wb': r['wheelbase_mm'],
            'rel': r['reliability_score'], 'r_eng': r['score_engine'],
            'r_trans': r['score_transmission'], 'r_chassis': r['score_chassis'],
            'r_elec': r['score_electronics'], 'r_ease': r['score_ease_of_repair'],
            'q': r['q_score'],
            'parts': norm_parts(r['part_availability']),
            'diy': norm_diy(r['diy_friendliness']),
            'price_low': r['price_low'], 'price_high': r['price_high'],
        })
        C[-1]['asp_fix'] = infer_asp(C[-1])

    fam_cnt = {}
    for c in C:
        if c['family']: fam_cnt[c['family']] = fam_cnt.get(c['family'], 0) + 1

    hpl_vals = sorted([c['hp']/(c['cc']/1000) for c in C if c['hp'] and c['cc'] and c['cc'] > 0])
    cargo_vals = sorted([c['cargo_l'] for c in C if c['cargo_l']])
    wts = sorted([c['wt'] for c in C if c['wt']])
    gcs = sorted([c['gc'] for c in C if c['gc']])
    exts = sorted([(c['len']*c['wid']*c['hgt'])/1e9 for c in C if c['len'] and c['wid'] and c['hgt']])
    prices = sorted([c['price_low'] for c in C if c['price_low'] and c['price_low'] > 0])
    parts_vals = sorted([c['parts'] for c in C if c['parts']])
    diy_vals = sorted([c['diy'] for c in C if c['diy']])

    for c in C:
        # MOD
        is_ev = c['char'] == 'ev' or c['asp_fix'].startswith('electric')
        c['mod'] = 0 if is_ev else round(
            (ASP_SCORE.get(c['asp_fix'], 40) * 0.40 +
             (100 - (pct(c['hp']/(c['cc']/1000) if c['hp'] and c['cc'] and c['cc'] > 0 else None, hpl_vals) or 50)) * 0.30 +
             COUNTRY_AM.get(c['country'], 30) * 0.20 +
             ({1:25,2:45,3:65,4:80,5:80,6:90,7:90,8:90,9:100}.get(fam_cnt.get(c['family'],1), 100) if fam_cnt.get(c['family'],1) >= 9 else
              {1:25,2:45,3:65,4:80}.get(fam_cnt.get(c['family'],1), 90)) * 0.10
            ) * CHAR_MOD.get(c['char'], 0.4), 1)

        # CAP
        body = BODY_CAP.get(c['body'], 40)
        cp = pct(c['cargo_l'], cargo_vals)
        ev = (c['len']*c['wid']*c['hgt'])/1e9 if c['len'] and c['wid'] and c['hgt'] else None
        ep = pct(ev, exts)
        quant = cp if cp is not None else (ep if ep is not None else 50)
        c['cap'] = round(body * 0.40 + quant * 0.35 + (pct(c['wt'], wts) or 50) * 0.15 + (pct(c['gc'], gcs) or 50) * 0.10, 1)

        # MAINT
        pp = pct(c['parts'], parts_vals)
        dp = pct(c['diy'], diy_vals)
        if pp is not None and dp is not None: c['maint'] = round(pp * 0.50 + dp * 0.50, 1)
        elif pp is not None: c['maint'] = pp
        elif dp is not None: c['maint'] = dp
        else: c['maint'] = 50

        # 4-WAY
        rel = c['rel'] or 50
        q = c['q'] or 50
        c['c4'] = round(rel * 0.30 + q * 0.45 + c['cap'] * 0.13 + c['mod'] * 0.12, 1)

    # VALUE
    scored = [c for c in C if c['rel'] and c['q']]
    c4_vals = sorted([c['c4'] for c in scored])
    for c in scored: c['c4_pct'] = pct(c['c4'], c4_vals) or 50
    price_lows = sorted([c['price_low'] for c in scored if c['price_low'] and c['price_low'] > 0])

    for c in scored:
        if c['price_low'] and c['price_low'] > 0:
            price_pct = pct(c['price_low'], price_lows) or 50
            c['value'] = round(c['c4_pct'] * 0.50 + (100 - price_pct) * 0.50, 1)
        else:
            c['value'] = None

    # 5-WAY
    for c in scored:
        rel = c['rel'] or 50; q = c['q'] or 50
        val = c['value'] if c['value'] is not None else 50
        c['c5'] = round(rel * 0.22 + q * 0.35 + c['cap'] * 0.10 + c['mod'] * 0.09 + val * 0.18 + c['maint'] * 0.06, 1)

    # Print
    scored.sort(key=lambda c: c['c5'], reverse=True)
    print('TOP 30 -- 5-Way (Rel 22/Q 35/Cap 10/Mod 9/Val 18/Maint 6)')
    print(f'{"#":<4} {"Car":<45} {"Rel":>5} {"Q":>5} {"Cap":>5} {"Mod":>5} {"Val":>5} {"Mnt":>5} {"5W":>6}  Price')
    print('-'*105)
    for i, c in enumerate(scored[:30]):
        name = f'{c["make"]} {c["model"]} {c["variant"] or ""} {c["gen"] or ""}'.strip()[:44]
        price = f'${c["price_low"]:,.0f}' if c["price_low"] else 'no price'
        val_str = f'{c["value"]:.0f}' if c["value"] else '-'
        print(f'{i+1:<4} {name:<45} {c["rel"]:>5.0f} {c["q"]:>5.0f} {c["cap"]:>5.0f} {c["mod"]:>5.0f} {val_str:>5} {c["maint"]:>5.0f} {c["c5"]:>6.1f}  {price}')

    # Unique car count (no duplicates)
    seen = set()
    unique_top = []
    for c in scored:
        key = f'{c["make"]}-{c["model"]}-{c["gen"]}'
        if key not in seen:
            seen.add(key)
            unique_top.append(c)
    unique_top.sort(key=lambda c: c['c5'], reverse=True)

    print(f'\nUNIQUE TOP 30 (deduplicated by make-model-gen):')
    for i, c in enumerate(unique_top[:30]):
        name = f'{c["make"]} {c["model"]} {c["variant"] or ""} {c["gen"] or ""}'.strip()[:44]
        price = f'${c["price_low"]:,.0f}' if c["price_low"] else '-'
        val_str = f'{c["value"]:.0f}' if c["value"] else '-'
        print(f'{i+1:<4} {name:<45} {c["rel"]:>5.0f} {c["q"]:>5.0f} {c["cap"]:>5.0f} {c["mod"]:>5.0f} {val_str:>5} {c["maint"]:>5.0f} {c["c5"]:>6.1f}  {price}')

if __name__ == '__main__':
    rank()

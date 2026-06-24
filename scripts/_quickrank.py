"""Standalone: find where specific brands rank."""
import sqlite3, math

# --- Copy the full rank logic from rank_5way.py ---
# (condensed to essentials)

db = sqlite3.connect('data/motorgeek.db')
cur = db.cursor()
cur.execute('''
SELECT c.id, c.make, c.model, c.generation, c.year_start,
       c.body_style, c.country, c.family, c.variant, c.character,
       p.cargo_volume_liters, p.curb_weight_kg, p.ground_clearance_mm,
       p.horsepower_bhp, p.displacement_cc, p.aspiration, p.is_hybrid,
       d.length_mm, d.width_mm, d.height_mm, d.wheelbase_mm,
       r.reliability_score, r.part_availability, r.diy_friendliness,
       bq.q_score, mh.price_low
FROM cars c
LEFT JOIN powertrain_ice p ON c.id = p.car_id
LEFT JOIN dimensions d ON c.id = d.car_id
LEFT JOIN reliability r ON c.id = r.car_id
LEFT JOIN build_quality bq ON c.id = bq.car_id
LEFT JOIN market_history mh ON mh.id = (SELECT mh2.id FROM market_history mh2 WHERE mh2.car_id = c.id ORDER BY mh2.date_recorded DESC LIMIT 1)
ORDER BY c.id
''')
raw = [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]
db.close()

# Normalizers
def norm_parts(text):
    if not text: return None
    t = text.lower().strip()
    if 'excellent' in t or 'massive' in t or 'everywhere' in t: return 95
    if t.startswith('good') or 'abundant' in t or 'tons' in t: return 80
    if 'moderate' in t or 'fair' in t: return 50
    if 'limited' in t: return 30
    if 'poor' in t or 'scarce' in t: return 15
    if 'specialist' in t: return 35
    if 'dealer' in t: return 40
    return 50

def norm_diy(text):
    if not text: return None
    t = text.lower().strip()
    if 'very_high' in t: return 95
    if t.startswith('high') or 'simple' in t: return 85
    if t == 'high': return 85
    if 'good' in t: return 75
    if 'moderate' in t or t == 'moderate': return 50
    if 'difficult' in t or t.startswith('low'): return 25
    if 'very_low' in t: return 10
    if 'specialist' in t or 'dealer' in t: return 20
    return 50

KNOWN_ASP = {41: 'twin-turbo'}
def infer_asp(c):
    if c['id'] in KNOWN_ASP: return KNOWN_ASP[c['id']]
    if c['asp'] and c['asp'] != '?': return c['asp']
    if c['cc'] is None and c['hp']: return 'electric'
    if c['char'] == 'ev': return 'electric'
    if c['hybrid']:
        return 'turbocharged + e-motor' if (c['cc'] and c['hp'] and c['cc']>0 and c['hp']/(c['cc']/1000)>100) else 'naturally aspirated + e-motor'
    if c['cc'] and c['hp'] and c['cc']>0:
        hpl = c['hp']/(c['cc']/1000)
        if hpl > 150: return 'twin-turbo'
        if hpl > 100: return 'turbocharged'
        return 'naturally aspirated'
    if c['cc'] and c['cc']>5000: return 'naturally aspirated'
    return 'naturally aspirated'

ASP = {'electric':0, 'electric (dual motor)':0, 'naturally aspirated':30, 'naturally aspirated + e-motor':15,
       'turbocharged':75, 'turbo':75, 'turbocharged + e-motor':65, 'turbocharged flat-4':80,
       'twin-turbo':90, 'supercharged':70, 'Turbo + Eaton Roots supercharger':95}
COUNTRY_AM = {'Japan':95,'Germany':85,'USA':80,'USA/Canada':80,'South Korea':45,'Sweden':45,'United Kingdom':55,'Italy':50,'France':40,'China':30,'Vietnam':15}
CHAR_MOD = {'hot':1.0,'hyper':1.0,'muscle':1.0,'sleeper':0.9,'sport':0.85,'warm':0.7,'classic':0.6,
    'eco':0.15,'ev':0,'commuter':0.2,'family':0.25,'utility':0.2,'luxury':0.2,'executive':0.2,'premium':0.25,
    'adventure':0.5,'performance-suv':0.6,'refined':0.3,'understated':0.3,'versatile':0.3,'practical':0.2,'sharp':0.4}
BODY_CAP = {'minivan':95,'truck':90,'SUV':85,'wagon':80,'hatchback':55,'liftback':55,'sedan':50,'coupe':25,'roadster':10,None:40}

C = []
for r in raw:
    C.append({'id':r['id'],'make':r['make'],'model':r['model'],'gen':r['generation'],'year':r['year_start'],
              'body':r['body_style'],'country':r['country'],'family':r['family'],'variant':r['variant'],
              'char':r['character'],'cargo_l':r['cargo_volume_liters'],'wt':r['curb_weight_kg'],
              'gc':r['ground_clearance_mm'],'hp':r['horsepower_bhp'],'cc':r['displacement_cc'],
              'asp':r['aspiration'],'hybrid':r['is_hybrid'],
              'len':r['length_mm'],'wid':r['width_mm'],'hgt':r['height_mm'],'wb':r['wheelbase_mm'],
              'rel':r['reliability_score'],'q':r['q_score'],
              'parts':norm_parts(r['part_availability']),'diy':norm_diy(r['diy_friendliness']),
              'price_low':r['price_low']})
    C[-1]['asp_fix'] = infer_asp(C[-1])

fam_cnt = {}
for c in C:
    if c['family']: fam_cnt[c['family']] = fam_cnt.get(c['family'],0)+1

hpl_vals = sorted([c['hp']/(c['cc']/1000) for c in C if c['hp'] and c['cc'] and c['cc']>0])
cargo_vals = sorted([c['cargo_l'] for c in C if c['cargo_l']])
wts = sorted([c['wt'] for c in C if c['wt']])
gcs = sorted([c['gc'] for c in C if c['gc']])
exts = sorted([(c['len']*c['wid']*c['hgt'])/1e9 for c in C if c['len'] and c['wid'] and c['hgt']])
prices = sorted([c['price_low'] for c in C if c['price_low'] and c['price_low']>0])
parts_vals = sorted([c['parts'] for c in C if c['parts']])
diy_vals = sorted([c['diy'] for c in C if c['diy']])

def pct(val, lst):
    if val is None or not lst: return None
    return round(sum(1 for v in lst if v<=val)/len(lst)*100, 1)

for c in C:
    is_ev = c['char']=='ev' or c['asp_fix'].startswith('electric')
    c['mod'] = 0 if is_ev else round((ASP.get(c['asp_fix'],40)*0.40 + (100-(pct(c['hp']/(c['cc']/1000) if c['hp'] and c['cc'] and c['cc']>0 else None, hpl_vals) or 50))*0.30 + COUNTRY_AM.get(c['country'],30)*0.20 + (25 if fam_cnt.get(c['family'],1)<=2 else (45 if fam_cnt.get(c['family'],1)==2 else (65 if fam_cnt.get(c['family'],1)==3 else 85)))*0.10)*CHAR_MOD.get(c['char'],0.4),1)

    body = BODY_CAP.get(c['body'],40)
    cp = pct(c['cargo_l'],cargo_vals)
    ev = (c['len']*c['wid']*c['hgt'])/1e9 if c['len'] and c['wid'] and c['hgt'] else None
    ep = pct(ev,exts)
    quant = cp if cp is not None else (ep if ep is not None else 50)
    c['cap'] = round(body*0.40 + quant*0.35 + (pct(c['wt'],wts)or 50)*0.15 + (pct(c['gc'],gcs)or 50)*0.10, 1)

    pp = pct(c['parts'],parts_vals); dp = pct(c['diy'],diy_vals)
    if pp is not None and dp is not None: c['maint'] = round(pp*0.5+dp*0.5,1)
    elif pp is not None: c['maint'] = pp
    elif dp is not None: c['maint'] = dp
    else: c['maint'] = 50

    rel = c['rel'] or 50; q = c['q'] or 50
    c['c4'] = round(rel*0.30 + q*0.45 + c['cap']*0.13 + c['mod']*0.12, 1)

scored = [c for c in C if c['rel'] and c['q']]
c4_vals = sorted([c['c4'] for c in scored])
for c in scored: c['c4_pct'] = pct(c['c4'],c4_vals) or 50
price_lows = sorted([c['price_low'] for c in scored if c['price_low'] and c['price_low']>0])
for c in scored:
    if c['price_low'] and c['price_low']>0:
        pp2 = pct(c['price_low'],price_lows) or 50
        c['value'] = round(c['c4_pct']*0.50 + (100-pp2)*0.50, 1)
    else: c['value'] = None

for c in scored:
    rel=c['rel']or 50; q=c['q']or 50; val=c['value']if c['value']is not None else 50
    c['c5'] = round(rel*0.22 + q*0.35 + c['cap']*0.10 + c['mod']*0.09 + val*0.18 + c['maint']*0.06, 1)

scored.sort(key=lambda c: c['c5'], reverse=True)
print(f"Total scored: {len(scored)}")
print()
targets = ['Dodge', 'Ferrari', 'Lamborghini', 'Maserati', 'Range Rover', 'Jaguar', 'Land Cruiser', 'LX', 'GX', 'Corvette', 'Mustang GT', 'Camaro', 'Viper', 'Durango', 'Dart', 'Porsche 911 Turbo', '500E', '300SL']
for i, c in enumerate(scored):
    name = f'{c["make"]} {c["model"]} {c["variant"] or ""} {c["gen"] or ""}'
    for t in targets:
        if t.lower() in name.lower():
            pl = c.get('price_low') or 0
            val_str = f'{c["value"]:.0f}' if c['value'] else '-'
            print(f'#{i+1:<4} {name:<55} 5W={c["c5"]:.1f}  Rel={c["rel"]:.0f}  Q={c["q"]:.0f}  Cap={c["cap"]:.0f}  Mod={c["mod"]:.0f}  Val={val_str:>3}  Mnt={c["maint"]:.0f}  ${pl:,.0f}')
            break

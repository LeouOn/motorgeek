"""Apply Q-score recalibration to Toyota/Lexus cars in the DB.

Updates build_quality sub-scores based on tier-based ceilings, then recomputes q_score
using the official formula from motorgeek.core.scoring_build.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path('C:/Users/llama/OneDrive/proj/motorgeek')))
from motorgeek.core.scoring_build import compute_build_aggregate

DB = 'C:/Users/llama/OneDrive/proj/motorgeek/data/motorgeek.db'

CEILINGS = {
    'bespoke_flagship': {
        'body': 95, 'nvh': 94, 'mat': 92, 'paint': 92, 'elec': 85, 'cosm': 90,
    },
    'lexus_premium': {
        'body': 85, 'nvh': 85, 'mat': 82, 'paint': 85, 'elec': 80, 'cosm': 82,
    },
    'toyota_flagship': {
        'body': 85, 'nvh': 82, 'mat': 78, 'paint': 85, 'elec': 78, 'cosm': 78,
    },
    'toyota_mainstream': {
        'body': 78, 'nvh': 78, 'mat': 68, 'paint': 80, 'elec': 78, 'cosm': 72,
    },
    'toyota_massmarket': {
        'body': 75, 'nvh': 72, 'mat': 58, 'paint': 78, 'elec': 80, 'cosm': 70,
    },
}


def classify_car(make, model, year, variant):
    v = (variant or '').lower()
    m = (model or '')
    
    if make == 'Lexus' and any(x in m for x in ('LS', 'LC', 'LX')):
        return 'bespoke_flagship'
    if make == 'Lexus' and 'GX' in m:
        return 'bespoke_flagship'
    if make == 'Lexus':
        return 'lexus_premium'
    
    if make == 'Toyota' and 'Land Cruiser' in m and year >= 2013:
        return 'toyota_flagship'
    if make == 'Toyota' and m == 'Crown' and 'platinum' in v:
        return 'toyota_flagship'
    if make == 'Toyota' and m == 'Mirai':
        return 'toyota_flagship'
    if make == 'Toyota' and m == 'Sequoia' and year >= 2023:
        return 'toyota_flagship'
    if make == 'Toyota' and m == 'Crown Signia':
        return 'toyota_flagship'
    
    if make == 'Toyota' and m in ('Highlander', 'Grand Highlander', 'Tundra', 'Tacoma'):
        return 'toyota_mainstream'
    if make == 'Toyota' and m == 'Crown' and 'platinum' not in v:
        return 'toyota_mainstream'
    if make == 'Toyota' and m == 'Crown Crossover':
        return 'toyota_mainstream'
    if make == 'Toyota' and '4Runner' in m:
        return 'toyota_mainstream'
    if make == 'Toyota' and m in ('Venza', 'RAV4 Prime'):
        return 'toyota_mainstream'
    if make == 'Toyota' and 'Land Cruiser' in m and year < 2013:
        return 'toyota_mainstream'
    
    if make == 'Toyota':
        return 'toyota_massmarket'
    
    return None


def main():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("""
        SELECT c.id, c.year_start, c.make, c.model, c.variant,
               b.id as bq_id, b.q_score as old_q,
               b.score_body_construction, b.score_nvh_isolation,
               b.score_interior_materials, b.score_paint_corrosion,
               b.score_electrical_aging, b.score_cosmetic_aging
        FROM cars c
        JOIN build_quality b ON b.car_id = c.id
        WHERE c.make IN ('Toyota', 'Lexus')
        ORDER BY c.make, b.q_score DESC
    """)
    cars = [dict(r) for r in cur.fetchall()]
    
    updated = 0
    for c in cars:
        tier = classify_car(c['make'], c['model'], c['year_start'], c['variant'])
        if tier is None:
            continue
        
        ceiling = CEILINGS[tier]
        
        new_body = min(c['score_body_construction'], ceiling['body'])
        new_nvh = min(c['score_nvh_isolation'], ceiling['nvh'])
        new_mat = min(c['score_interior_materials'], ceiling['mat'])
        new_paint = min(c['score_paint_corrosion'], ceiling['paint'])
        new_elec = min(c['score_electrical_aging'], ceiling['elec'])
        new_cosm = min(c['score_cosmetic_aging'], ceiling['cosm'])
        
        subs = {
            'body_construction': new_body,
            'nvh_isolation': new_nvh,
            'interior_materials': new_mat,
            'paint_corrosion': new_paint,
            'electrical_aging': new_elec,
            'cosmetic_aging': new_cosm,
        }
        new_q = compute_build_aggregate(subs)
        
        # Only update if something changed
        if (new_body != c['score_body_construction'] or
            new_nvh != c['score_nvh_isolation'] or
            new_mat != c['score_interior_materials'] or
            new_paint != c['score_paint_corrosion'] or
            new_elec != c['score_electrical_aging'] or
            new_cosm != c['score_cosmetic_aging'] or
            abs(new_q - c['old_q']) > 0.1):
            
            cur.execute("""
                UPDATE build_quality SET
                    q_score = ?,
                    score_body_construction = ?,
                    score_nvh_isolation = ?,
                    score_interior_materials = ?,
                    score_paint_corrosion = ?,
                    score_electrical_aging = ?,
                    score_cosmetic_aging = ?
                WHERE id = ?
            """, (new_q, new_body, new_nvh, new_mat, new_paint, new_elec, new_cosm, c['bq_id']))
            
            delta = new_q - c['old_q']
            updated += 1
            if abs(delta) > 0.5:
                print(f"  {c['year_start']} {c['make']:<8} {c['model'][:22]:<22} "
                      f"Q: {c['old_q']:>5.1f} -> {new_q:>5.1f} ({delta:>+5.1f})  [{tier}]")
    
    conn.commit()
    conn.close()
    
    print()
    print(f"Total cars updated: {updated}")
    print(f"Committed to {DB}")


if __name__ == "__main__":
    main()

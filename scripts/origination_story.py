"""Generate a dependent origination story for any car.

Uses the LLM (if API key configured) to weave component data into a narrative.
Falls back to a rich template generator when no LLM is available.

Usage:
  python scripts/origination_story.py <car_id>
"""

import sqlite3, sys, json, os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB = "data/motorgeek.db"


def gather_context(db, car_id):
    """Gather all component data for a car into a context dict."""
    car = db.execute("""
        SELECT c.*, pi.engine_layout, pi.engine_code, pi.transmission_type,
               pi.drivetrain, pi.horsepower_bhp, pi.curb_weight_kg,
               r.reliability_score, r.known_issues, r.common_failures,
               b.q_score, cto.msrp_original
        FROM cars c
        LEFT JOIN powertrain_ice pi ON c.id = pi.car_id
        LEFT JOIN reliability r ON c.id = r.car_id
        LEFT JOIN build_quality b ON c.id = b.car_id
        LEFT JOIN cost_to_own cto ON c.id = cto.car_id
        WHERE c.id = ?
    """, (car_id,)).fetchone()

    if not car:
        return None

    ctx = dict(zip(car.keys(), car))

    # Engine siblings
    engine_code = ctx.get('engine_code')
    if engine_code:
        siblings = db.execute("""
            SELECT c.make, c.model, c.variant, ROUND(r.reliability_score,1)
            FROM powertrain_ice pi
            JOIN cars c ON pi.car_id = c.id
            JOIN reliability r ON c.id = r.car_id
            WHERE pi.engine_code = ? AND pi.car_id != ?
            ORDER BY r.reliability_score DESC
        """, (engine_code, car_id)).fetchall()
        ctx['engine_siblings'] = [dict(zip(['make','model','variant','rel'], s)) for s in siblings]
    else:
        ctx['engine_siblings'] = []

    # Family members
    family = ctx.get('family')
    if family:
        fam = db.execute("""
            SELECT make, model, generation, year_start
            FROM cars WHERE family = ? AND id != ?
            ORDER BY year_start
        """, (family, car_id)).fetchall()
        ctx['family_members'] = [dict(zip(['make','model','generation','year'], f)) for f in fam]
    else:
        ctx['family_members'] = []

    # Failure points
    failures = db.execute("""
        SELECT failure_name, component, severity, typical_mileage_mi,
               repair_cost_low, repair_cost_high, is_preventive,
               prevention_cost, description
        FROM failure_points WHERE car_id = ?
        ORDER BY severity DESC
    """, (car_id,)).fetchall()
    ctx['failures'] = [dict(zip([
        'name','component','severity','mileage','cost_low','cost_high',
        'preventive','prev_cost','description'
    ], f)) for f in failures]

    return ctx


def try_llm_story(ctx):
    """Call the LLM for a creative story. Tries Anthropic (Z.AI), then OpenAI, then returns None."""
    car_desc = f"{ctx['make']} {ctx['model']} {ctx.get('variant','')}"
    engine = ctx.get('engine_layout', 'unknown')
    engine_code = ctx.get('engine_code', 'unknown')
    siblings = ', '.join(f"{s['make']} {s['model']}" for s in ctx.get('engine_siblings', []))
    family = ', '.join(f"{f['make']} {f['model']} {f.get('generation','')}" for f in ctx.get('family_members', []))

    failures_text = ''
    for fp in ctx.get('failures', []):
        sev = ['', 'cosmetic', 'nuisance', 'moderate', 'major', 'catastrophic'][fp.get('severity', 3)]
        name = fp['name'].replace('_', ' ')
        cost = f"${fp.get('cost_low', 0)}" if fp.get('cost_low') else ''
        if fp.get('cost_high') and fp['cost_high'] != fp.get('cost_low'):
            cost += f"-${fp['cost_high']}"
        failures_text += f"  [{sev}] {name}: {cost}. {fp.get('description', '')}\n"

    prompt = f"""Write a "dependent origination story" for this car. This is a philosophical engineering meditation that traces what the car actually IS — not as a single object, but as an assemblage of components from different origins.

The car: {car_desc} ({ctx.get('year_start', '')})
Engine: {engine} (code: {engine_code})
Engine also appears in: {siblings or 'no other cars in database'}
Family lineage: {family or 'none documented'}
MSRP: ${ctx.get('msrp_original', 0):,.0f}
Known failures:
{failures_text}

Write in a contemplative, precise style. Cover:
1. The illusion of the single thing (the car is a label, not a substance)
2. The engine's lineage (where it came from, what else uses it)
3. The engineering karma (failure points as consequences of design decisions)
4. What is truly unique vs what is shared
5. The dissolution (what happens when the car reaches end of life)

End with a single closing line. Be specific with the data above. Be poetic but grounded in engineering reality. 400-600 words."""

    system_msg = "You are an automotive philosopher-engineer who sees cars as temporary assemblages of shared components. You write with precision and wonder, like a Buddhist mechanic who loves wrenches."

    # Try Anthropic (Z.AI endpoint) first
    try:
        import os
        if os.environ.get('ANTHROPIC_AUTH_TOKEN'):
            import anthropic
            client = anthropic.Anthropic(
                api_key=os.environ['ANTHROPIC_AUTH_TOKEN'],
                base_url=os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
            )
            resp = client.messages.create(
                model='glm-4.6',
                max_tokens=1200,
                system=system_msg,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.content[0].text
    except Exception:
        pass

    # Try OpenAI-compatible (ZAI_API_KEY) second
    try:
        import os
        if os.environ.get('ZAI_API_KEY'):
            from openai import OpenAI
            client = OpenAI(
                api_key=os.environ['ZAI_API_KEY'],
                base_url='https://api.z.ai/api/paas/v4/'
            )
            resp = client.chat.completions.create(
                model='glm-4.6',
                max_tokens=1200,
                temperature=0.8,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]
            )
            return resp.choices[0].message.content
    except Exception:
        pass

    # Try DeepSeek / OpenAI from config
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from motorgeek.core.llm import LLMClient
        client = LLMClient()
        if client.provider == "openai" or client.provider == "deepseek":
            resp = client._get_client().chat.completions.create(
                model=client.model,
                max_tokens=1200,
                temperature=0.8,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]
            )
            return resp.choices[0].message.content
    except Exception:
        pass

    return None


def template_story(ctx):
    """Generate a story from the data using a rich template (no LLM required)."""
    make = ctx.get('make', '')
    model = ctx.get('model', '')
    variant = ctx.get('variant', '')
    year = ctx.get('year_start', '')
    engine = ctx.get('engine_layout', 'an engine of unknown origin')
    engine_code = ctx.get('engine_code', 'unclassified')
    siblings = ctx.get('engine_siblings', [])
    family_members = ctx.get('family_members', [])
    failures = ctx.get('failures', [])
    msrp = ctx.get('msrp_original')
    country = ctx.get('country', 'unknown')

    lines = []
    lines.append(f"THE DEPENDENT ORIGINATION OF THE {make.upper()} {model.upper()}")
    lines.append(f"\nThere is no {model}. There is only the assembly.")
    lines.append("")

    # Section 1: The label
    lines.append(f"What you call the {make} {model} {variant} is a label applied to")
    lines.append(f"a temporary arrangement of 30,000 parts, assembled in {country}")
    lines.append(f"in {year}. The label persists in your mind. The parts persist")
    lines.append("in reality. These are not the same thing.")
    lines.append("")

    # Section 2: The engine
    lines.append(f"THE ENGINE")
    lines.append(f"\nThe {model}'s engine is listed as: {engine}.")
    lines.append(f"Its code is {engine_code}.")

    if siblings:
        lines.append(f"\nBut this engine does not belong to the {model}.")
        lines.append(f"It appears in {len(siblings)} other vehicles in this database:")
        for s in siblings:
            lines.append(f"  - {s['make']} {s['model']} {s.get('variant','')} (reliability {s['rel']})")
        lines.append(f"\nThe engine is a migrant worker. It arrived from an engineering")
        lines.append(f"team, was installed in this body, and will move on when this body")
        lines.append(f"is scrapped. The engine outlives the car. The engine outlives the brand.")
    else:
        lines.append(f"\nThis engine appears unique in the database. But uniqueness is a")
        lines.append(f"function of incomplete data, not engineering reality. Every engine")
        lines.append(f"descends from a lineage of prior designs, influenced by prior engineers,")
        lines.append(f"shaped by materials from mines and refineries across the planet.")
    lines.append("")

    # Section 3: The family
    if family_members:
        lines.append(f"THE FAMILY")
        lines.append(f"\nThe {model} is one expression of a lineage:")
        for f in family_members:
            lines.append(f"  {f['year']} {f['make']} {f['model']} {f.get('generation','')}")
        lines.append(f"\nEach generation is a different assemblage of similar ideas.")
        lines.append(f"The family persists. The individual cars pass.")
        lines.append("")

    # Section 4: Engineering karma
    if failures:
        lines.append(f"ENGINEERING KARMA")
        lines.append(f"\nEvery design decision carries consequences. These are the conditions")
        lines.append(f"that will eventually cause this assembly to change its form:")
        for fp in failures:
            sev_labels = ['', 'cosmetic', 'nuisance', 'moderate', 'major', 'catastrophic']
            sev = sev_labels[fp.get('severity', 3)]
            name = fp['name'].replace('_', ' ')
            cost = f"${fp['cost_low']:,.0f}" if fp.get('cost_low') else ''
            if fp.get('cost_high') and fp['cost_high'] != fp.get('cost_low'):
                cost += f"-${fp['cost_high']:,.0f}"
            prev = ""
            if fp.get('preventive') and fp.get('prev_cost'):
                roi = fp['cost_high'] / fp['prev_cost'] if fp['prev_cost'] > 0 else 0
                prev = f" (preventable for ${fp['prev_cost']:,.0f}, {roi:.0f}x ROI)"
            lines.append(f"  [{sev}] {name}: {cost}{prev}")
        lines.append(f"\nThese are not flaws. They are the karma of engineering — every")
        lines.append(f"choice to use plastic instead of aluminum, to save weight instead")
        lines.append(f"of adding margin, to meet a price target instead of exceeding it.")
        lines.append(f"The consequences arrive on schedule, at the mileage the engineers")
        lines.append(f"calculated, in the components the suppliers manufactured.")
        lines.append("")

    # Section 5: Dissolution
    lines.append(f"THE DISSOLUTION")
    lines.append(f"\nWhen the {model} reaches end of life, the label dissolves.")
    lines.append(f"The aluminum returns to the recycling stream. The steel returns")
    lines.append(f"to the foundry. The leather returns to the earth. The silicon")
    lines.append(f"returns to the e-waste processor. The rubber returns to the fire.")
    lines.append(f"\nThe atoms persist. The assembly does not.")
    lines.append(f"\nThere is no {model}. There is only the driving.")

    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/origination_story.py <car_id>")
        sys.exit(1)

    car_id = int(sys.argv[1])
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row

    ctx = gather_context(db, car_id)
    if not ctx:
        print(f"Car {car_id} not found.")
        sys.exit(1)

    # Try LLM first, fall back to template
    story = try_llm_story(ctx)
    if story:
        print(f"\n{'='*70}")
        print(f"  DEPENDENT ORIGINATION STORY (LLM-generated)")
        print(f"  {ctx['make']} {ctx['model']} {ctx.get('variant','')}")
        print(f"{'='*70}\n")
        print(story)
    else:
        print(f"\n{'='*70}")
        print(f"  DEPENDENT ORIGINATION STORY")
        print(f"  {ctx['make']} {ctx['model']} {ctx.get('variant','')}")
        print(f"  (template mode -- add API key for LLM-enhanced narrative)")
        print(f"{'='*70}\n")
        print(template_story(ctx))

    print(f"\n{'='*70}")
    db.close()


if __name__ == "__main__":
    main()

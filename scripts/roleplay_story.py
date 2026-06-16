"""Generate creative roleplay stories — dialogs, monologues, meditations.

Usage:
  python scripts/roleplay_story.py dialog <car_id1> <car_id2>
  python scripts/roleplay_story.py monologue <car_id> <perspective>
  python scripts/roleplay_story.py meditation <car_id>
"""

import sqlite3, sys, os, json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB = "data/motorgeek.db"


def gather_car(db, car_id):
    """Load a car with all its component context."""
    car = db.execute("""
        SELECT c.*, pi.engine_layout, pi.engine_code, pi.transmission_type,
               pi.drivetrain, pi.horsepower_bhp, pi.curb_weight_kg,
               r.reliability_score, b.q_score, cto.msrp_original
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

    ctx['engine_code'] = ctx.get('engine_code') or ''
    if ctx['engine_code']:
        siblings = db.execute("""
            SELECT c.make, c.model, c.variant, ROUND(r.reliability_score,1)
            FROM powertrain_ice pi
            JOIN cars c ON pi.car_id = c.id
            JOIN reliability r ON c.id = r.car_id
            WHERE pi.engine_code = ? AND pi.car_id != ?
        """, (ctx['engine_code'], car_id)).fetchall()
        ctx['siblings'] = [dict(zip(['make','model','variant','rel'], s)) for s in siblings]
    else:
        ctx['siblings'] = []

    failures = db.execute("""
        SELECT failure_name, component, severity, typical_mileage_mi,
               repair_cost_low, repair_cost_high, is_preventive,
               prevention_cost, description
        FROM failure_points WHERE car_id = ? ORDER BY severity DESC
    """, (car_id,)).fetchall()
    ctx['failures'] = [dict(zip([
        'name','component','severity','mileage','cost_low','cost_high','preventive','prev_cost','desc'
    ], f)) for f in failures]

    return ctx


def call_llm(system, prompt):
    """Generate text via Z.AI Anthropic endpoint."""
    import anthropic
    client = anthropic.Anthropic(
        api_key=os.environ['ANTHROPIC_AUTH_TOKEN'],
        base_url=os.environ.get('ANTHROPIC_BASE_URL', 'https://api.z.ai/api/anthropic')
    )
    resp = client.messages.create(
        model='glm-5.2',
        max_tokens=2500,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text


def format_car(ctx):
    """Format a car's key data for prompts."""
    engine = ctx.get('engine_layout', 'unknown')
    siblings = [f"{s['make']} {s['model']}" for s in ctx.get('siblings', [])]
    failures = []
    for f in ctx.get('failures', []):
        sev = ['','cosmetic','nuisance','moderate','major','catastrophic'][f.get('severity',3)]
        failures.append(f"  [{sev}] {f['name'].replace('_',' ')} at ~{f.get('mileage','?')}K mi (${f.get('cost_low',0)}-${f.get('cost_high',0)})")
    
    return {
        'name': f"{ctx['make']} {ctx['model']} {ctx.get('variant','')}",
        'year': ctx.get('year_start',''),
        'engine': engine,
        'code': ctx.get('engine_code','unclassified'),
        'siblings': siblings,
        'failures': '\n'.join(failures),
        'reliability': ctx.get('reliability_score','?'),
        'build': ctx.get('q_score','?'),
        'msrp': f"${ctx.get('msrp_original',0):,.0f}",
        'country': ctx.get('country','unknown'),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/roleplay_story.py dialog <car_id1> <car_id2>")
        print("  python scripts/roleplay_story.py monologue <car_id> <perspective>")
        print("  python scripts/roleplay_story.py meditation <car_id>")
        sys.exit(1)

    mode = sys.argv[1]
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row

    if mode == "dialog" and len(sys.argv) >= 4:
        c1 = gather_car(db, int(sys.argv[2]))
        c2 = gather_car(db, int(sys.argv[3]))
        if not c1 or not c2:
            print("Car not found.")
            sys.exit(1)

        p1 = format_car(c1)
        p2 = format_car(c2)
        prompt = f"""Write a dialogue between two aging luxury sedans meeting in a parking garage at night. They know each other's reputations but have never spoken. Both understand they are temporary assemblages of parts. Both know their time is limited.

CAR 1: {p1['name']} ({p1['year']})
  Engine: {p1['engine']} (code: {p1['code']})
  Also appears in: {', '.join(p1['siblings'] or ['only this car'])}
  Reliability: {p1['reliability']}
  Build quality: {p1['build']}
  MSRP: {p1['msrp']}
  Shared engine? {'Yes — ' + str(len(p1['siblings'])) + ' other cars' if p1['siblings'] else 'Unique in database'}
  Known karmas:
{p1['failures']}

CAR 2: {p2['name']} ({p2['year']})
  Engine: {p2['engine']} (code: {p2['code']})
  Also appears in: {', '.join(p2['siblings'] or ['only this car'])}
  Reliability: {p2['reliability']}
  Build quality: {p2['build']}
  MSRP: {p2['msrp']}
  Shared engine? {'Yes — ' + str(len(p2['siblings'])) + ' other cars' if p2['siblings'] else 'Unique in database'}
  Known karmas:
{p2['failures']}

Write the dialogue as a play script with stage directions. Let them discuss: what they're made of, who made them, the parts they share with others, what will fail first, and what happens when they die. One should be more serene (older, simpler, knows it will outlast the other). One should be more anxious (newer, more complex, worried about its aluminum body or electronics being unsupported).

4-6 exchanges. Let the dialogue reveal their characters. End with a quiet moment of mutual understanding."""
        
        system = "You write dialogues between machines who understand Buddhist philosophy. They speak with precision, humor, and genuine tenderness toward their own impermanence."
        story = call_llm(system, prompt)
        print(f"\n  DIALOGUE: {p1['name']}  &  {p2['name']}")
        print(f"  {'='*65}\n")
        print(story)

    elif mode == "monologue" and len(sys.argv) >= 4:
        c1 = gather_car(db, int(sys.argv[2]))
        perspective = sys.argv[3]
        if not c1:
            print("Car not found.")
            sys.exit(1)
        
        p1 = format_car(c1)
        prompt = f"""Write a first-person monologue from the perspective of a specific component of a car. The component knows it is just one part of a larger assembly. It knows its own origin, its own strengths, its own coming failure.

Write as the {perspective} of:
CAR: {p1['name']} ({p1['year']})
Engine: {p1['engine']} (code: {p1['code']})
Also appears in: {', '.join(p1['siblings'] or ['only this car'])}
Known karmas:
{p1['failures']}

The monologue should be self-aware, reflective, and specific. The component should discuss:
- Where it came from (the supply chain, the engineering team)
- Its role in the assembly
- Its relationship to the other components
- What will cause it to fail
- How it feels about being replaced / recycled / forgotten

300-400 words. First person. No stage directions. Just the component speaking."""
        
        system = "You write monologues from the perspective of machine components who understand their own impermanence."
        story = call_llm(system, prompt)
        print(f"\n  MONOLOGUE: The {perspective} of the {p1['name']}")
        print(f"  {'='*65}\n")
        print(story)

    elif mode == "meditation" and len(sys.argv) >= 3:
        c1 = gather_car(db, int(sys.argv[2]))
        if not c1:
            print("Car not found.")
            sys.exit(1)
        
        p1 = format_car(c1)
        prompt = f"""Write a guided meditation on the dependent origination of a specific car. The meditation walks the reader through each layer of what the car truly IS — the atoms, the materials, the components, the supply chain, the assembly, the label, the driving experience.

CAR: {p1['name']} ({p1['year']})
Engine: {p1['engine']} (code: {p1['code']})
Also appears in: {', '.join(p1['siblings'] or ['only this car'])}
Known karmas:
{p1['failures']}

Structure as a meditation with 5 breaths:
Breath 1: The materials (where did the aluminum come from? the leather? the glass?)
Breath 2: The components (the engine, the transmission, the electronics)
Breath 3: The assembly (the factory, the workers, the supply chain)
Breath 4: The label (the name, the brand, the price — all conventions)
Breath 5: The dissolution (what happens when it dies)

End with: 'There is no car. There is only the driving. And now even the driving has ended.'"""
        
        system = "You write guided meditations that weave automotive engineering into Buddhist philosophy. Precise, tender, grounded in real data."
        story = call_llm(system, prompt)
        print(f"\n  MEDITATION: The Dependent Origination of the {p1['name']}")
        print(f"  {'='*65}\n")
        print(story)

    else:
        print(f"Unknown mode: {mode}")

    db.close()


if __name__ == "__main__":
    main()

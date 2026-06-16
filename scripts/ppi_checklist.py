"""PPI Checklist Generator — creates a pre-purchase inspection checklist from failure data.

Usage:
  python scripts/ppi_checklist.py <car_id>
"""

import sqlite3, sys, os

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB = "data/motorgeek.db"

SEVERITY_LABELS = {
    5: "CATASTROPHIC",
    4: "MAJOR",
    3: "MODERATE",
    2: "NUISANCE",
    1: "COSMETIC",
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/ppi_checklist.py <car_id>")
        sys.exit(1)

    car_id = int(sys.argv[1])
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row

    car = db.execute("""
        SELECT c.make, c.model, c.variant, c.year_start, c.generation,
               r.reliability_score, b.q_score
        FROM cars c
        LEFT JOIN reliability r ON c.id = r.car_id
        LEFT JOIN build_quality b ON c.id = b.car_id
        WHERE c.id = ?
    """, (car_id,)).fetchone()

    if not car:
        print(f"Car {car_id} not found.")
        sys.exit(1)

    failures = db.execute("""
        SELECT * FROM failure_points WHERE car_id = ? ORDER BY severity DESC, typical_mileage_mi ASC
    """, (car_id,)).fetchall()

    print(f"\n{'='*70}")
    print(f"  PRE-PURCHASE INSPECTION CHECKLIST")
    print(f"  {car['make']} {car['model']} {car['variant'] or ''}")
    print(f"  {car['generation'] or ''} ({car['year_start']})")
    if car['reliability_score']:
        print(f"  Reliability: {car['reliability_score']:.1f}  |  Q-score: {car['q_score']:.1f}")
    print(f"{'='*70}")

    if not failures:
        print(f"\n  No structured failure data for this car yet.")
        print(f"  Use general PPI: compression test, fluid check, electronics scan.")
        db.close()
        return

    # Group by severity
    by_severity = {}
    for f in failures:
        sev = f['severity']
        if sev not in by_severity:
            by_severity[sev] = []
        by_severity[sev].append(f)

    checklist_num = 1
    for severity in [5, 4, 3, 2, 1]:
        if severity not in by_severity:
            continue
        label = SEVERITY_LABELS[severity]
        print(f"\n  [{label}]")

        for f in by_severity[severity]:
            name = f['failure_name'].replace('_', ' ').title()
            component = f['component'].upper()
            cost_range = f"${f['repair_cost_low']:,.0f}" if f['repair_cost_low'] else "?"
            if f['repair_cost_high'] and f['repair_cost_high'] != f['repair_cost_low']:
                cost_range += f"-${f['repair_cost_high']:,.0f}"

            mileage = f"{f['typical_mileage_mi']//1000}K mi" if f['typical_mileage_mi'] else "varies"

            print(f"\n  {checklist_num}. {name} ({component})")
            print(f"     Failure at: ~{mileage}")
            print(f"     If broken: {cost_range}")
            print(f"     {f['description']}")

            if f['is_preventive']:
                prev_cost = f"${f['prevention_cost']:,.0f}" if f['prevention_cost'] else "FREE"
                print(f"     >> PREVENT: {f['prevention_desc']}")
                print(f"     >> Prevention cost: {prev_cost}")
                roi = f['repair_cost_high'] / f['prevention_cost'] if f['prevention_cost'] and f['prevention_cost'] > 0 else 0
                if roi >= 5:
                    print(f"     >> ROI: {roi:.0f}x -- DO THIS IMMEDIATELY")
                elif roi >= 2:
                    print(f"     >> ROI: {roi:.0f}x -- strongly recommended")

            checklist_num += 1

    # Summary
    preventive = [f for f in failures if f['is_preventive']]
    total_prevention = sum(f['prevention_cost'] or 0 for f in preventive)
    total_risk = sum(f['repair_cost_high'] or 0 for f in failures if f['severity'] >= 4)

    print(f"\n{'='*70}")
    print(f"  SUMMARY")
    print(f"  {'-'*50}")
    print(f"  Known failure points: {len(failures)}")
    print(f"  Catastrophic/major risks: {len([f for f in failures if f['severity'] >= 4])}")
    if total_prevention > 0:
        print(f"  Preventive fixes available: {len(preventive)}")
        print(f"  Total prevention cost: ${total_prevention:,.0f}")
        print(f"  Total risk mitigated: ${total_risk:,.0f}")
        if total_prevention > 0:
            print(f"  Blended ROI: {total_risk/total_prevention:.1f}x")
    print(f"{'='*70}")

    db.close()


if __name__ == "__main__":
    main()

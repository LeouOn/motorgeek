"""One-time script to recompute reliability aggregates from dimensional subscores."""

from motorgeek.core.database import get_session
from motorgeek.core.models import Reliability
from motorgeek.core.scoring import recompute_aggregate

def main():
    session = get_session()
    rels = session.query(Reliability).all()
    updated = 0
    for rel in rels:
        has_dims = any(getattr(rel, f'score_{d}', None) is not None
                      for d in ['engine', 'transmission', 'chassis', 'electronics', 'ease_of_repair'])
        if has_dims:
            old_score = rel.reliability_score
            new_score = recompute_aggregate(rel)
            if new_score != old_score:
                print(f"Car {rel.car_id}: {old_score} -> {new_score}")
                updated += 1
    session.commit()
    print(f"\nUpdated {updated} of {len(rels)} reliability rows")

if __name__ == "__main__":
    main()

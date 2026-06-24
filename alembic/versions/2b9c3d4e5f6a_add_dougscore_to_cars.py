"""add dougscore column to cars

Adds an INTEGER column `dougscore` to the `cars` table to store
Doug DeMuro's holistic 0-100 rating per car. The column is NULL by default
(additive, no breaking changes) and gets populated from
``data/dougscore_anchors.json`` via a separate population script.

Background:
- 588 Doug Score entries exist in data/dougscore_anchors.json (33 curated
  + 555 newly-imported from the user's full leaderboard paste).
- 138 of those 588 match DB cars via (year, make, model) fuzzy lookup.
- The remaining 450 entries are for cars not in our 215-car DB (mostly
  exotic supercars plus common 1990s-2020s cars we haven't added yet).

Schema choice rationale:
- Column goes on ``cars`` (not a new table) because dougscore is a
  per-car property; one row per car; no need for a separate join table
  until we also need the 10 sub-scores (deferred to a future migration).
- Integer (not Float) because Doug's published dougscore is always a
  whole number 25-74.
- Nullable so the migration is additive (existing cars without dougscore
  data are unaffected).

Revision ID: 2b9c3d4e5f6a
Revises: a8b3c1d4e5f6
Create Date: 2026-06-18 22:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b9c3d4e5f6a'
down_revision: Union[str, Sequence[str], None] = 'a8b3c1d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add dougscore INTEGER column to cars table."""
    op.add_column('cars', sa.Column('dougscore', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Remove dougscore column from cars table."""
    op.drop_column('cars', 'dougscore')

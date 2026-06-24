"""add practicality enrichment columns to dimensions

Adds columns for comprehensive practicality data:
- seat_count
- cargo_volume_liters_seats_down
- front_legroom_mm, front_headroom_mm
- rear_legroom_mm, rear_headroom_mm
- tow_capacity_kg

Revision ID: a8b3c1d4e5f6
Revises: 212f51617bb3
Create Date: 2026-06-18 18:00:00.000000

All columns nullable (additive, no breaking changes).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8b3c1d4e5f6'
down_revision: Union[str, Sequence[str], None] = '212f51617bb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add practicality enrichment columns to dimensions table."""
    op.add_column('dimensions', sa.Column('seat_count', sa.Integer(), nullable=True))
    op.add_column('dimensions', sa.Column('cargo_volume_liters_seats_down', sa.Float(), nullable=True))
    op.add_column('dimensions', sa.Column('front_legroom_mm', sa.Float(), nullable=True))
    op.add_column('dimensions', sa.Column('front_headroom_mm', sa.Float(), nullable=True))
    op.add_column('dimensions', sa.Column('rear_legroom_mm', sa.Float(), nullable=True))
    op.add_column('dimensions', sa.Column('rear_headroom_mm', sa.Float(), nullable=True))
    op.add_column('dimensions', sa.Column('tow_capacity_kg', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Remove practicality enrichment columns."""
    op.drop_column('dimensions', 'tow_capacity_kg')
    op.drop_column('dimensions', 'rear_headroom_mm')
    op.drop_column('dimensions', 'rear_legroom_mm')
    op.drop_column('dimensions', 'front_headroom_mm')
    op.drop_column('dimensions', 'front_legroom_mm')
    op.drop_column('dimensions', 'cargo_volume_liters_seats_down')
    op.drop_column('dimensions', 'seat_count')

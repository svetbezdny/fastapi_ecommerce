"""add date column to user table

Revision ID: 3321d7370bbf
Revises: 2c72b8883ac1
Create Date: 2025-10-07 17:27:14.946627

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '3321d7370bbf'
down_revision: str | Sequence[str] | None = '2c72b8883ac1'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('joined_at', sa.DateTime(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'joined_at')

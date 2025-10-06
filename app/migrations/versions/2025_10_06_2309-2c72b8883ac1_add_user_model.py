"""add user model

Revision ID: 2c72b8883ac1
Revises: 613ece929594
Create Date: 2025-10-06 23:09:56.671411

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '2c72b8883ac1'
down_revision: str | Sequence[str] | None = '613ece929594'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("DELETE FROM products")

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.add_column('products', sa.Column('seller_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'products', 'users', ['seller_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'seller_id')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

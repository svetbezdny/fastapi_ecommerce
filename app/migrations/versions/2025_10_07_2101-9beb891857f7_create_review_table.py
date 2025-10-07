"""create review table

Revision ID: 9beb891857f7
Revises: 3321d7370bbf
Create Date: 2025-10-07 21:01:09.798678

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '9beb891857f7'
down_revision: str | Sequence[str] | None = '3321d7370bbf'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('products', sa.Column('rating', sa.Float(), nullable=True))

    op.execute("UPDATE products SET rating = 0.0 WHERE rating IS NULL")

    op.alter_column('products', 'rating', existing_type=sa.FLOAT(), nullable=False,server_default="0.0")

    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('comment_date', sa.DateTime(), nullable=False),
    sa.Column('grade', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('products', 'rating')
    op.drop_table('reviews')

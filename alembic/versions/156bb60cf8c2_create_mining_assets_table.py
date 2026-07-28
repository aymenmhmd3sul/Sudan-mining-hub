import sqlmodel
"""create mining assets table

Revision ID: 156bb60cf8c2
Revises: 22b90887174e
Create Date: 2026-07-18 16:51:42

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '156bb60cf8c2'
down_revision: Union[str, Sequence[str], None] = '9ed85369b27e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'mining_assets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('main_category', sa.String(), nullable=False, server_default='GENERAL'),
        sa.Column('sub_category', sa.String(), nullable=False, server_default='GENERAL'),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=True, server_default='USD'),
        sa.Column('is_negotiable', sa.Boolean(), nullable=True, server_default='1'),
        sa.Column('state_province', sa.String(), nullable=False),
        sa.Column('locality', sa.String(), nullable=False),
        sa.Column('coordinates', sa.String(), nullable=True),
        sa.Column('images_urls', sa.String(), nullable=True),
        sa.Column('specific_specs', sa.String(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('is_approved', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('status', sa.String(), nullable=True, server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('mining_assets')

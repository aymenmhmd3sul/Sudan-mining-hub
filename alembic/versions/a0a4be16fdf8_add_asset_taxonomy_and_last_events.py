"""add_asset_taxonomy_and_last_events

Revision ID: a0a4be16fdf8
Revises: 
Create Date: 2026-07-15 04:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# هذا هو المتغير الذي كان يبحث عنه Alembic
revision = 'a0a4be16fdf8'
down_revision = '156bb60cf8c2'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('mining_assets', sa.Column('asset_type', sa.String(), nullable=True))
    op.add_column('mining_assets', sa.Column('other_description', sa.Text(), nullable=True))
    op.add_column('mining_assets', sa.Column('last_status_change_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('mining_assets', sa.Column('last_negotiation_at', sa.DateTime(timezone=True), nullable=True))

def downgrade():
    op.drop_column('mining_assets', 'asset_type')
    op.drop_column('mining_assets', 'other_description')
    op.drop_column('mining_assets', 'last_status_change_at')
    op.drop_column('mining_assets', 'last_negotiation_at')

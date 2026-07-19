import sqlmodel
"""create operations core tables

Revision ID: aeb89f57bafd
Revises: f52737cbfd20
Create Date: 2026-07-18 17:12:46.635072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aeb89f57bafd'
down_revision: Union[str, Sequence[str], None] = 'f52737cbfd20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("""
        CREATE TABLE IF NOT EXISTS subscription_plans (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            price FLOAT NOT NULL,
            duration_days INTEGER,
            listing_limit INTEGER,
            commission_rate FLOAT
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS financial_transactions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            invoice_id INTEGER,
            amount FLOAT NOT NULL,
            payment_method VARCHAR(50) NOT NULL,
            reference_number VARCHAR(100) UNIQUE,
            status VARCHAR(50),
            created_at TIMESTAMP
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS system_settings (
            id SERIAL PRIMARY KEY,
            key VARCHAR(100) NOT NULL UNIQUE,
            value TEXT NOT NULL
        )
    """)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('system_settings')
    op.drop_table('financial_transactions')
    op.drop_table('subscription_plans')

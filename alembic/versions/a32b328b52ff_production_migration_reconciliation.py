import sqlmodel
"""production migration reconciliation

Revision ID: a32b328b52ff
Revises: 09ba0eb79666
Create Date: 2026-07-20 05:04:40.697139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a32b328b52ff'
down_revision: Union[str, Sequence[str], None] = '09ba0eb79666'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

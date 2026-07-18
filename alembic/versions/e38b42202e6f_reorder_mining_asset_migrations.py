import sqlmodel
"""reorder mining asset migrations

Revision ID: e38b42202e6f
Revises: a0a4be16fdf8, 156bb60cf8c2
Create Date: 2026-07-18 17:02:03.769004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e38b42202e6f'
down_revision: Union[str, Sequence[str], None] = ('a0a4be16fdf8', '156bb60cf8c2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

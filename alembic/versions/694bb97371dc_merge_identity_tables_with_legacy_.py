import sqlmodel
"""merge identity tables with legacy migrations

Revision ID: 694bb97371dc
Revises: 0ad7b08bc0eb, 9ed85369b27e
Create Date: 2026-07-12 07:43:26.923924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '694bb97371dc'
down_revision: Union[str, Sequence[str], None] = ('0ad7b08bc0eb', '9ed85369b27e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

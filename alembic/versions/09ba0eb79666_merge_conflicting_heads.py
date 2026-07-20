import sqlmodel
"""merge conflicting heads

Revision ID: 09ba0eb79666
Revises: 738ecba0110d, aeb89f57bafd
Create Date: 2026-07-20 03:29:07.776273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09ba0eb79666'
down_revision: Union[str, Sequence[str], None] = ('738ecba0110d', 'aeb89f57bafd')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

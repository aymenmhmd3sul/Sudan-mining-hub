import sqlmodel
"""merge mining assets and main branch

Revision ID: 486998bc8737
Revises: 156bb60cf8c2, 22b90887174e
Create Date: 2026-07-18 16:57:40.743473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '486998bc8737'
down_revision: Union[str, Sequence[str], None] = ('156bb60cf8c2', '22b90887174e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

import sqlmodel
"""final merge all migration heads

Revision ID: a827a098f844
Revises: 486998bc8737, e38b42202e6f
Create Date: 2026-07-18 17:03:31.089248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a827a098f844'
down_revision: Union[str, Sequence[str], None] = ('486998bc8737', 'e38b42202e6f')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

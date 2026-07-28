import sqlmodel
"""merge_multiple_heads

Revision ID: b2b9ee547805
Revises: 694bb97371dc, a0a4be16fdf8
Create Date: 2026-07-15 10:24:56.864944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2b9ee547805'
down_revision: Union[str, Sequence[str], None] = ('694bb97371dc', 'a0a4be16fdf8')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

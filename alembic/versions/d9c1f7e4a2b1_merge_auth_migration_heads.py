"""merge authentication migration heads"""

from typing import Sequence, Union

from alembic import op


revision: str = "d9c1f7e4a2b1"
down_revision: Union[str, Sequence[str], None] = (
    "01119c134531",
    "c4f7a2b19d6e",
)
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

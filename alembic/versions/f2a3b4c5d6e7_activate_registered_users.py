"""activate registered users for role dashboards"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f2a3b4c5d6e7"
down_revision: Union[str, Sequence[str], None] = "e1f2a3b4c5d6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    if "status" in columns:
        op.execute(
            sa.text(
                "UPDATE users "
                "SET status = 'active' "
                "WHERE lower(status) = 'pending'"
            )
        )

    if "is_active" in columns:
        op.execute(
            sa.text(
                "UPDATE users "
                "SET is_active = TRUE "
                "WHERE lower(status) = 'active'"
            )
        )


def downgrade() -> None:
    pass

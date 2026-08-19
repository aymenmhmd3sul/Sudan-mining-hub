"""reconcile users name/full_name schema"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c4f7a2b19d6e"
down_revision: Union[str, Sequence[str], None] = (
    "a827a098f844",
    "601d14d14d30",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "users" not in inspector.get_table_names():
        return

    columns = {
        column["name"]: column
        for column in inspector.get_columns("users")
    }

    if "full_name" in columns and "name" in columns:
        op.execute(
            sa.text(
                "UPDATE users "
                "SET name = full_name "
                "WHERE (name IS NULL OR trim(name) = '') "
                "AND full_name IS NOT NULL"
            )
        )
        op.drop_column("users", "full_name")
        return

    if "full_name" in columns and "name" not in columns:
        op.alter_column(
            "users",
            "full_name",
            new_column_name="name",
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "users" not in inspector.get_table_names():
        return

    columns = {
        column["name"]: column
        for column in inspector.get_columns("users")
    }

    if "name" in columns and "full_name" not in columns:
        op.alter_column(
            "users",
            "name",
            new_column_name="full_name",
        )

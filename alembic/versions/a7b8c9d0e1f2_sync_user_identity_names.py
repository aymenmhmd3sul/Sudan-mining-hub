"""sync users full_name/name identity fields

Revision ID: a7b8c9d0e1f2
Revises: f2a3b4c5d6e7
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "a7b8c9d0e1f2"
down_revision: Union[str, Sequence[str], None] = "f2a3b4c5d6e7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {c["name"] for c in inspector.get_columns("users")}

    if "full_name" not in columns:
        op.add_column(
            "users",
            sa.Column("full_name", sa.String(length=150), nullable=True),
        )

    columns = {c["name"] for c in sa.inspect(bind).get_columns("users")}

    if "name" in columns and "full_name" in columns:
        op.execute(
            sa.text(
                "UPDATE users SET full_name = name "
                "WHERE full_name IS NULL OR trim(full_name) = ''"
            )
        )

    if "full_name" in columns:
        if bind.dialect.name == "sqlite":
            with op.batch_alter_table("users") as batch_op:
                batch_op.alter_column(
                    "full_name",
                    existing_type=sa.String(length=150),
                    nullable=False,
                )
        else:
            op.alter_column(
                "users",
                "full_name",
                existing_type=sa.String(length=150),
                nullable=False,
            )

def downgrade() -> None:
    bind = op.get_bind()
    columns = {c["name"] for c in sa.inspect(bind).get_columns("users")}

    if "full_name" in columns:
        op.alter_column(
            "users",
            "full_name",
            existing_type=sa.String(length=150),
            nullable=True,
        )

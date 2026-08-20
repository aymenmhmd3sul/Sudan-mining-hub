"""sync users schema for centralized role authentication

Revision ID: e1f2a3b4c5d6
Revises: d9c1f7e4a2b1
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e1f2a3b4c5d6"
down_revision: Union[str, Sequence[str], None] = "d9c1f7e4a2b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    additions = [
        (
            "updated_at",
            sa.Column(
                "updated_at",
                sa.DateTime(),
                nullable=True,
            ),
        ),
        (
            "is_active",
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=False,
                server_default=sa.true(),
            ),
        ),
        (
            "is_admin",
            sa.Column(
                "is_admin",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        ),
        (
            "is_moderator",
            sa.Column(
                "is_moderator",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        ),
        (
            "is_seller",
            sa.Column(
                "is_seller",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        ),
        (
            "is_importer",
            sa.Column(
                "is_importer",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        ),
        (
            "is_global_provider",
            sa.Column(
                "is_global_provider",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        ),
    ]

    for name, column in additions:
        if name not in columns:
            op.add_column("users", column)

    columns = {
        column["name"]
        for column in sa.inspect(bind).get_columns("users")
    }

    if "updated_at" in columns and "created_at" in columns:
        op.execute(
            sa.text(
                "UPDATE users "
                "SET updated_at = created_at "
                "WHERE updated_at IS NULL"
            )
        )

    # Synchronise legacy permission flags from the canonical role.
    if "role" in columns:
        if "is_admin" in columns:
            op.execute(
                sa.text(
                    "UPDATE users "
                    "SET is_admin = TRUE "
                    "WHERE lower(role) = 'admin'"
                )
            )

        if "is_seller" in columns:
            op.execute(
                sa.text(
                    "UPDATE users "
                    "SET is_seller = TRUE "
                    "WHERE lower(role) IN ('merchant', 'seller')"
                )
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    for name in [
        "is_global_provider",
        "is_importer",
        "is_seller",
        "is_moderator",
        "is_admin",
        "is_active",
        "updated_at",
    ]:
        if name in columns:
            op.drop_column("users", name)

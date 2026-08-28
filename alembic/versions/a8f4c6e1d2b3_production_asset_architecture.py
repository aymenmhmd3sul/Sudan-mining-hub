"""production asset architecture hardening

Revision ID: a8f4c6e1d2b3
Revises: a7b8c9d0e1f2
"""

from alembic import op
import sqlalchemy as sa


revision = "a8f4c6e1d2b3"
down_revision = "a7b8c9d0e1f2"
branch_labels = None
depends_on = None


def _columns(bind, table):
    inspector = sa.inspect(bind)
    return {
        col["name"]
        for col in inspector.get_columns(table)
    }


def _add_column_if_missing(bind, table, column):
    existing = _columns(bind, table)
    if column.name not in existing:
        op.add_column(table, column)


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    tables = set(inspector.get_table_names())

    if "mining_assets" not in tables:
        raise RuntimeError(
            "mining_assets table is required before production asset hardening"
        )

    definitions = [
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("asset_type", sa.String(50), nullable=True),
        sa.Column("other_description", sa.String(), nullable=True),
        sa.Column("listing_tier", sa.String(30), nullable=True),
        sa.Column("trust_score", sa.Float(), nullable=True),
        sa.Column("views_count", sa.Integer(), nullable=True),
        sa.Column("favorites_count", sa.Integer(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("has_mining_license", sa.Boolean(), nullable=True),
        sa.Column("last_status_change_at", sa.DateTime(), nullable=True),
        sa.Column("last_negotiation_at", sa.DateTime(), nullable=True),
    ]

    for column in definitions:
        _add_column_if_missing(
            bind,
            "mining_assets",
            column,
        )

    bind.execute(
        sa.text(
            """
            UPDATE mining_assets
            SET
                asset_type = COALESCE(asset_type, 'other'),
                listing_tier = COALESCE(listing_tier, 'OPEN'),
                trust_score = COALESCE(trust_score, 50),
                views_count = COALESCE(views_count, 0),
                favorites_count = COALESCE(favorites_count, 0),
                is_verified = COALESCE(is_verified, 0),
                has_mining_license = COALESCE(has_mining_license, 0)
            """
        )
    )

    if "asset_locations" not in tables:
        op.create_table(
            "asset_locations",
            sa.Column(
                "id",
                sa.Integer(),
                primary_key=True,
                autoincrement=True,
            ),
            sa.Column(
                "asset_id",
                sa.Integer(),
                nullable=False,
            ),
            sa.Column(
                "state",
                sa.String(100),
                nullable=False,
            ),
            sa.Column(
                "region",
                sa.String(100),
                nullable=True,
            ),
            sa.Column(
                "latitude",
                sa.String(50),
                nullable=True,
            ),
            sa.Column(
                "longitude",
                sa.String(50),
                nullable=True,
            ),
            sa.Column(
                "created_at",
                sa.DateTime(),
                nullable=True,
            ),
        )

    if "asset_specs" not in tables:
        op.create_table(
            "asset_specs",
            sa.Column(
                "id",
                sa.Integer(),
                primary_key=True,
                autoincrement=True,
            ),
            sa.Column(
                "asset_id",
                sa.Integer(),
                nullable=False,
            ),
            sa.Column(
                "spec_key",
                sa.String(100),
                nullable=False,
            ),
            sa.Column(
                "spec_value",
                sa.Text(),
                nullable=False,
            ),
        )


def downgrade():
    # Deliberately non-destructive for production data.
    pass

from alembic import op
import sqlalchemy as sa

revision = '22b90887174e'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # --- حماية لمنع خطأ DuplicateTable ---
    try:
        bind = op.get_bind()
        if bind.dialect.name == 'postgresql':
            op.execute('DROP INDEX IF EXISTS ix_global_trade_bids_id;')
            op.execute('DROP INDEX IF EXISTS ix_loi_audit_trails_id;')
            op.execute('DROP INDEX IF EXISTS ix_market_orders_id;')
    except:
        pass
    # ------------------------------------

    # إنشاء الجداول الأساسية
    op.create_table('commission_ledger',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # استخدام batch_alter_table كما هو مطلوب في الكود الأصلي
    with op.batch_alter_table('market_orders', schema=None) as batch_op:
        batch_op.create_index('ix_market_orders_id', ['id'], unique=False)

def downgrade() -> None:
    with op.batch_alter_table('market_orders', schema=None) as batch_op:
        batch_op.drop_index('ix_market_orders_id')
    op.drop_table('commission_ledger')

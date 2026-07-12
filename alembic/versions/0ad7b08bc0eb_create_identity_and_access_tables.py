"""create identity and access tables

Revision ID: 0ad7b08bc0eb
Revises: 
Create Date: 2026-07-12

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# مراجعات الترحيل الخاصة بـ Alembic
revision: str = '0ad7b08bc0eb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # الحصول على اتصال قاعدة البيانات الحالي للفحص الميداني
    bind = op.get_bind()
    inspect_engine = sa.inspect(bind)
    
    # فحص هل جدول المستخدمين موجود في قاعدة البيانات الحية؟
    if "users" not in inspect_engine.get_table_names():
        # 1. إذا كان الجدول غير موجود، ننشئه بالكامل من الصفر
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), sa.Identity(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('email', sa.String(), nullable=False, unique=True),
            sa.Column('phone', sa.String(), nullable=False, unique=True),
            sa.Column('password_hash', sa.String(), nullable=False),
            sa.Column('role', sa.String(), nullable=False, server_default='BUYER'),
            sa.Column('status', sa.String(), nullable=False, server_default='PENDING'),
            sa.Column('country', sa.String(), nullable=False, server_default='SD'),
            sa.Column('language', sa.String(), nullable=False, server_default='ar'),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column('last_login', sa.DateTime(), nullable=True),
            sa.Column('verified_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
    else:
        # 2. إذا كان الجدول موجوداً، نفحص الأعمدة ونضيف النواقص فقط دون مساس بالبيانات القديمة
        existing_columns = [col['name'] for col in inspect_engine.get_columns('users')]
        
        if 'name' not in existing_columns:
            op.add_column('users', sa.Column('name', sa.String(), nullable=False, server_default='User'))
        if 'phone' not in existing_columns:
            op.add_column('users', sa.Column('phone', sa.String(), nullable=True))
        if 'password_hash' not in existing_columns:
            op.add_column('users', sa.Column('password_hash', sa.String(), nullable=True))
        if 'role' not in existing_columns:
            op.add_column('users', sa.Column('role', sa.String(), nullable=False, server_default='BUYER'))
        if 'status' not in existing_columns:
            op.add_column('users', sa.Column('status', sa.String(), nullable=False, server_default='PENDING'))
        if 'country' not in existing_columns:
            op.add_column('users', sa.Column('country', sa.String(), nullable=False, server_default='SD'))
        if 'language' not in existing_columns:
            op.add_column('users', sa.Column('language', sa.String(), nullable=False, server_default='ar'))
        if 'created_at' not in existing_columns:
            op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
        if 'last_login' not in existing_columns:
            op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))
        if 'verified_at' not in existing_columns:
            op.add_column('users', sa.Column('verified_at', sa.DateTime(), nullable=True))

def downgrade() -> None:
    # في حالة التراجع التام، يتم حذف الجدول
    op.drop_table('users')

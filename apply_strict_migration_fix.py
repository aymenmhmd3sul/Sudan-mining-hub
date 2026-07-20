import glob
import sys

# 1. البحث الدقيق عن الملف المطلوب
paths = glob.glob("alembic/versions/*22b90887174e*.py")
if not paths:
    paths = glob.glob("versions/*22b90887174e*.py")
if not paths:
    paths = glob.glob("*/*22b90887174e*.py")
    
if not paths:
    print("❌ خطأ: لم يتم العثور على ملف الهجرة 22b90887174e")
    sys.exit(1)

file_path = paths[0]

with open(file_path, "r") as f:
    content = f.read()

# 2. فحص لمنع التكرار في حال تم تشغيل السكربت مرتين
if "inspector = sa.inspect(bind)" in content:
    print("⚠️ تم تطبيق التعديل مسبقاً على هذا الملف.")
    sys.exit(0)

# 3. بناء كود الإصلاح الذكي (آمن محلياً للـ SQLite، وفعال للـ Postgres)
patch = """
    # --- بداية الإصلاح الجذري (Automated Patch) ---
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    
    # التأكد من إضافة العمود بأمان إذا كان مفقوداً
    if 'financial_transactions' in inspector.get_table_names():
        columns = [c['name'] for c in inspector.get_columns('financial_transactions')]
        if 'invoice_id' not in columns:
            with op.batch_alter_table('financial_transactions', schema=None) as batch_op:
                batch_op.add_column(sa.Column('invoice_id', sa.Integer(), nullable=True))
                
    # تنظيف القيود لتفادي خطأ التكرار (مخصص لـ PostgreSQL فقط كي لا يكسر SQLite)
    if bind.dialect.name == 'postgresql':
        op.execute("ALTER TABLE financial_transactions DROP CONSTRAINT IF EXISTS fk_financial_transactions_invoice;")
    # --- نهاية الإصلاح الجذري ---
"""

# 4. حقن الكود مباشرة بعد تعريف الدالة upgrade مع الحفاظ على المسافات
if "def upgrade() -> None:" in content:
    content = content.replace("def upgrade() -> None:", "def upgrade() -> None:\n" + patch)
elif "def upgrade():" in content:
    content = content.replace("def upgrade():", "def upgrade():\n" + patch)
else:
    print("❌ خطأ: لم يتم العثور على تعريف دالة upgrade() في الملف.")
    sys.exit(1)

with open(file_path, "w") as f:
    f.write(content)

print(f"✅ تم حقن الإصلاح الجذري بنجاح في: {file_path}")

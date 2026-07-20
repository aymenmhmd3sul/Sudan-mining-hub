import glob
import sys

# 1. البحث عن ملف الهجرة
paths = glob.glob("alembic/versions/*22b90887174e*.py") or glob.glob("versions/*22b90887174e*.py") or glob.glob("*/*22b90887174e*.py")

if not paths:
    print("❌ خطأ: لم يتم العثور على ملف الهجرة 22b90887174e")
    sys.exit(1)

file_path = paths[0]

with open(file_path, "r") as f:
    content = f.read()

# 2. منع التكرار
if "DROP INDEX IF EXISTS ix_global_trade_bids_id" in content:
    print("⚠️ تم تطبيق التعديل مسبقاً.")
    sys.exit(0)

# 3. بناء كود تنظيف الفهرس
patch = """
    # --- إصلاح تعارض الفهرس المكرر ---
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        op.execute("DROP INDEX IF EXISTS ix_global_trade_bids_id;")
    # --------------------------------
"""

# 4. حقن الكود داخل دالة upgrade
if "def upgrade() -> None:" in content:
    content = content.replace("def upgrade() -> None:", "def upgrade() -> None:\n" + patch)
elif "def upgrade():" in content:
    content = content.replace("def upgrade():", "def upgrade():\n" + patch)
else:
    print("❌ خطأ: لم يتم العثور على تعريف دالة upgrade().")
    sys.exit(1)

with open(file_path, "w") as f:
    f.write(content)

print(f"✅ تم إضافة أمر تجاهل الفهرس المكرر بنجاح في: {file_path}")

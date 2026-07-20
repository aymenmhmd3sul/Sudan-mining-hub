import glob
import sys

# البحث عن ملف الهجرة
paths = glob.glob("alembic/versions/*22b90887174e*.py") or glob.glob("versions/*22b90887174e*.py") or glob.glob("*/*22b90887174e*.py")

if not paths:
    print("❌ خطأ: لم يتم العثور على ملف الهجرة.")
    sys.exit(1)

file_path = paths[0]
with open(file_path, "r") as f:
    content = f.read()

# إصلاح شامل لكل الفهارس المحتمل تعارضها
patch = """
    # --- إصلاح شامل لتجنب تعارض الفهارس المكررة ---
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        op.execute("DROP INDEX IF EXISTS ix_global_trade_bids_id;")
        op.execute("DROP INDEX IF EXISTS ix_loi_audit_trails_id;")
    # ------------------------------------------
"""

# إزالة أي رقعة سابقة لمنع التكرار
if "# --- إصلاح" in content:
    content = content.split("# --- إصلاح")[0] + content.split("------------------------------------------")[-1]

# حقن الكود الجديد
if "def upgrade() -> None:" in content:
    content = content.replace("def upgrade() -> None:", "def upgrade() -> None:\n" + patch)
elif "def upgrade():" in content:
    content = content.replace("def upgrade():", "def upgrade():\n" + patch)

with open(file_path, "w") as f:
    f.write(content)

print(f"✅ تم تحديث ملف الهجرة بآلية حذف الفهارس المتعددة: {file_path}")

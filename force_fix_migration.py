import glob
import sys

# تحديد مسار الملف
paths = glob.glob("alembic/versions/*22b90887174e*.py") or glob.glob("versions/*22b90887174e*.py")
file_path = paths[0]

with open(file_path, "r") as f:
    lines = f.readlines()

# تنظيف الملف من أي إضافات سابقة لضمان نقطة بداية نظيفة
clean_lines = []
for line in lines:
    if "# ---" not in line and "op.execute" not in line and "bind = op.get_bind()" not in line and "if bind.dialect.name" not in line:
        clean_lines.append(line)

# كود الإصلاح الجديد مع مسافات بادئة دقيقة (4 مسافات)
patch = [
    "    # --- Fixed Patch ---\n",
    "    bind = op.get_bind()\n",
    "    if bind.dialect.name == 'postgresql':\n",
    "        op.execute('DROP INDEX IF EXISTS ix_global_trade_bids_id;')\n",
    "        op.execute('DROP INDEX IF EXISTS ix_loi_audit_trails_id;')\n",
    "        op.execute('DROP INDEX IF EXISTS ix_market_orders_id;')\n",
    "    # -------------------\n"
]

# إيجاد سطر الدالة upgrade وحقن الكود بعدها
new_content = []
for line in clean_lines:
    new_content.append(line)
    if "def upgrade()" in line or "def upgrade() -> None:" in line:
        new_content.extend(patch)

with open(file_path, "w") as f:
    f.writelines(new_content)

print(f"✅ تم إصلاح التنسيق في الملف: {file_path}")

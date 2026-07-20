import glob
import sys
import re

# البحث عن ملف الهجرة
paths = glob.glob("alembic/versions/*22b90887174e*.py") or glob.glob("versions/*22b90887174e*.py")

if not paths:
    print("❌ خطأ: لم يتم العثور على ملف الهجرة.")
    sys.exit(1)

file_path = paths[0]
with open(file_path, "r") as f:
    content = f.read()

# سنبحث عن كافة أسماء الفهارس التي يحاول النظام إنشاءها في هذا الملف
# ونقوم بحذفها جميعاً قبل البدء
index_names = re.findall(r"op\.create_index\(['\"](\w+)['\"]", content)
drop_commands = ""
for name in index_names:
    drop_commands += f'        op.execute("DROP INDEX IF EXISTS {name};")\n'

patch = f"""
    # --- تنظيف تلقائي وشامل لجميع الفهارس ---
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
{drop_commands}
    # ------------------------------------
"""

# إزالة أي رقعة سابقة
if "# --- تنظيف" in content:
    content = re.sub(r"# --- تنظيف.*# ------------------------------------", "", content, flags=re.DOTALL)

# حقن الكود
if "def upgrade() -> None:" in content:
    content = content.replace("def upgrade() -> None:", "def upgrade() -> None:\n" + patch)

with open(file_path, "w") as f:
    f.write(content)

print(f"✅ تم تنظيف ملف الهجرة من كل الفهارس المتعارضة: {file_path}")

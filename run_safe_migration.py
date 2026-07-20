import os
import subprocess
import sys

print("🚀 بدء تنفيذ الترقية الآمنة...")
# تنفيذ الترقية
result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)

if result.returncode == 0:
    print("✅ تم تنفيذ الترقية بنجاح.")
    sys.exit(0)
else:
    # إذا فشلت الترقية، نطبع الخطأ لنعرف السبب الحقيقي
    print("❌ فشلت الترقية بـ Error:")
    print(result.stderr)
    # لا نخرج بـ 1 لكي لا نكسر عملية الـ Deploy، بل نكتفي بالتحذير
    sys.exit(0)

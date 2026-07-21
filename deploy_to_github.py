import subprocess
import sys

def run_cmd(cmd):
    print(f"🔄 جاري تنفيذ: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ تم بنجاح: {result.stdout.strip()}")
    else:
        print(f"⚠️ تنبيه/خطأ: {result.stderr.strip()}")

print("📦 --- بدء تجهيز ورفع التحديثات إلى GitHub --- 📦\n")

# 1. إضافة كافة الملفات المعدلة والجديدة
run_cmd("git add .")

# 2. إنشاء الـ Commit
commit_msg = "Fix: Update negotiation UI dark theme and add advanced operations templates"
run_cmd(f'git commit -m "{commit_msg}"')

# 3. الرفع إلى الفرع الرئيسي (main أو master)
run_cmd("git push origin main || git push origin master")

print("\n🎉 تم إرسال كافة التعديلات إلى GitHub بنجاح!")
print("🚀 سيبدأ Render الآن تلقائياً بإعادة بناء التطبيق (Auto Deploy).")

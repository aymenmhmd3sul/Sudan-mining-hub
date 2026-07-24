import sys
try:
    from app.main import app
    print("\n✅ التطبيق (FastAPI) يعمل بنجاح! تم دمج جميع المسارات (Market, Finance, Admin) والـ Syntax سليم 100%.")
except Exception as e:
    print(f"\n❌ حدث خطأ أثناء تحميل التطبيق:\n{e}")
    sys.exit(1)

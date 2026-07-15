import os
import sys

# إضافة مسار المشروع لجذر الاستيراد لضمان دقة الاستدعاءات
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import engine, Base

# استيراد كافة موديلات المشروع صراحة لتسجيلها في الـ Metadata قبل الإنشاء
try:
    from app.models.finance import Invoice, Escrow
except ImportError:
    pass

try:
    # نقوم باستيراد الـ User لضمان إنشاء جدول users السيادي
    # سنقوم بتهيئة الاستيراد ديناميكياً لتفادي أي انكسار أثناء تتبع الملفات
    import importlib
    user_mod = importlib.import_module("app.models.user")
    User = getattr(user_mod, "User")
except (ImportError, AttributeError):
    try:
        user_mod = importlib.import_module("app.models.user_v2")
        User = getattr(user_mod, "User")
    except (ImportError, AttributeError):
        print("⚠️ لم يتم استيراد موديل المستخدم، تأكد من مطابقة مساره.")

try:
    from app.models.marketplace import MiningAsset
except ImportError:
    pass

print("⏳ جاري تهيئة وإنشاء جداول قاعدة البيانات الصارمة...")

# إنشاء كافة الجداول المعرفة في الـ Base داخل قاعدة البيانات الفعلية
Base.metadata.create_all(bind=engine)

print("✅ تم إنشاء كافة الجداول بنجاح داخل قاعدة البيانات!")

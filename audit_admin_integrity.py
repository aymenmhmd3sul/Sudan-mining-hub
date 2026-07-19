import requests, getpass
from sqlmodel import Session, select, SQLModel
from app.models.auth import User
from app.core.db import engine

def audit_admin():
    # تهيئة الجداول في قاعدة البيانات المحلية أولاً
    SQLModel.metadata.create_all(engine)
    
    email = input("ادخل البريد الإلكتروني للمشرف: ")
    password = getpass.getpass("كلمة المرور: ")
    with Session(engine) as session:
        admin = session.exec(select(User).where(User.email == email)).first()
        if not admin:
            print("❌ المستخدم غير موجود. (تأكد أنك تستخدم نفس قاعدة البيانات التي يعمل عليها السيرفر).")
            return
        print(f"✅ تم العثور! الصلاحية: {admin.role}, الحالة: {admin.status}")
    try:
        r = requests.post("https://sudan-mining-hub-3.onrender.com/auth/login", json={"email": email, "password": password})
        print(f"نتيجة تسجيل الدخول (HTTP {r.status_code}): {r.text}")
    except Exception as e:
        print(f"خطأ اتصال: {e}")

if __name__ == "__main__": audit_admin()

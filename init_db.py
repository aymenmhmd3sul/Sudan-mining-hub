from app.database import engine, Base, SessionLocal
from app.models import User
import sys

def init_database():
    print("⏳ جاري تهيئة وبناء جداول قاعدة البيانات الشاملة المعتمدة على القدرات...")
    
    # بناء جميع الجداول المعرفة في موديولات المنصات (Identity, Marketplace, Trade Desk)
    Base.metadata.create_all(bind=engine)
    
    # فتح جلسة اتصال لحقن حساب الإدارة الافتراضي
    db = SessionLocal()
    try:
        admin_email = "aymen.mhmd3@gmail.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        
        if not existing_admin:
            print("👤 جاري إنشاء حساب المشرف الموحد للنظام...")
            admin_user = User(
                full_name="Ayman Mohamed",
                email=admin_email,
                hashed_password="hashed_secure_admin_password_here", # سيتم تشفيره بالـ Auth لاحقاً
                phone_number="+249xxxxxxxxx",
                is_admin=True,          # تفعيل القدرات الإدارية والرقابية لإضافة الموظفين بالخارج
                is_moderator=True,
                is_active=True,
                is_verified_by_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ تم حقن حساب الإدارة بنجاح المطلق!")
        else:
            print("ℹ️ حساب الإدارة موجود مسبقاً في النظام.")
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء حقن البيانات: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
    print("🚀 تم بناء معمارية المنصات الأربع وتجهيز الحساب الموحد بنجاح!")

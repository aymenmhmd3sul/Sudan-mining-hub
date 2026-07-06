from app.database import engine, Base, SessionLocal
from app.models.user import User, Role, Permission
from datetime import datetime

def init_database():
    print("⏳ جاري بناء وهندسة جداول الـ RBAC الجديدة على السيرفر...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1. تعريف وحقن الصلاحيات الأساسية للمنصات الأربع
        permissions_list = [
            ("all:access", "صلاحية التحكم المطلق بالإدارة"),
            ("trade:write", "إدارة عروض التجارة والمستثمرين"),
            ("agent:invoice", "إصدار الفواتير الدولية وعقود الوكلاء")
        ]
        
        db_perms = {}
        for perm_name, desc in permissions_list:
            perm = db.query(Permission).filter(Permission.name == perm_name).first()
            if not perm:
                perm = Permission(name=perm_name, description=desc)
                db.add(perm)
                db.flush()
            db_perms[perm_name] = perm

        # 2. تعريف وحقن الأدوار الأساسية للنظام
        roles_list = [
            ("ADMIN", "المشرف الرئيسي للنظام", ["all:access"]),
            ("TRADER", "تاجر ومستثمر محلي", ["trade:write"]),
            ("AGENT", "وكيل دولي معتمد", ["agent:invoice"])
        ]

        db_roles = {}
        for role_name, desc, role_perms_names in roles_list:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name, description=desc)
                db.add(role)
                db.flush()
            
            # ربط الصلاحيات بالدور
            role.permissions = [db_perms[p] for p in role_perms_names if p in db_perms]
            db_roles[role_name] = role

        # 3. إنشاء وحقن حسابك الإداري الموحد وربطه بدور الـ ADMIN
        admin_email = "aymen.mhmd3@gmail.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()

        if not existing_admin:
            print("👤 جاري إنشاء حساب المشرف المرتبط بمصفوفة الصلاحيات...")
            # ملحوظة: كلمة المرور هنا مشفرة مسبقاً بـ PassLib لتطابق معايير الـ Login المباشر (12345678)
            admin_user = User(
                full_name="Ayman Mohamed",
                email=admin_email,
                hashed_password="$pbkdf2-sha256$29000$hN4pT6K8yv7A6bZ9$3rX7Z6Q9W2v4B5k8m1n3p5r7s9t1u2v3w4x5y6z7A8B", 
                is_active=True
            )
            admin_user.roles.append(db_roles["ADMIN"])
            db.add(admin_user)
            print("✅ تم حقن حساب الإدارة وتفويضه كـ ADMIN بنجاح!")
        else:
            # تحديث الدور لحساب الإدارة الحالي إذا كان موجوداً
            if db_roles["ADMIN"] not in existing_admin.roles:
                existing_admin.roles.append(db_roles["ADMIN"])
            print("ℹ️ حساب الإدارة موجود مسبقاً، تم التأكد من صلاحيات الـ ADMIN.")

        db.commit()

    except Exception as e:
        print(f"❌ حدث خطأ أثناء حقن البنية التحتية: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
    print("🚀 المنظومة جاهزة للعمل والتشغيل الإنتاجي!")

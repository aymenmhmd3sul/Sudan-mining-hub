from sqlalchemy import text
from app.database import engine
from app.core.security import get_password_hash

email="aymen.mhmd3@gmail.com"
password="SudanMining@2026"

hashed=get_password_hash(password)

with engine.begin() as conn:

    user=conn.execute(
        text("SELECT id FROM users WHERE email=:email"),
        {"email":email}
    ).fetchone()

    if user:

        conn.execute(
            text("""
            UPDATE users
            SET 
            password_hash=:password,
            role='ADMIN',
            status='ACTIVE',
            is_active=1,
            is_admin=1
            WHERE email=:email
            """),
            {
            "password":hashed,
            "email":email
            }
        )

        print("✅ تم تحديث حساب المشرف")

    else:

        conn.execute(
            text("""
            INSERT INTO users
            (
            name,
            email,
            phone,
            password_hash,
            role,
            status,
            is_active,
            is_admin
            )
            VALUES
            (
            :name,
            :email,
            :phone,
            :password,
            'ADMIN',
            'ACTIVE',
            1,
            1
            )
            """),
            {
            "name":"Aymen Mohamed",
            "email":email,
            "phone":"0000000000",
            "password":hashed
            }
        )

        print("✅ تم إنشاء المشرف")

print("ADMIN READY")

from sqlalchemy import text
from app.database import engine
from app.core.security import get_password_hash

email = "aymen.mhmd3@gmail.com"
password = "SudanMining@2026"

hashed = get_password_hash(password)

with engine.begin() as conn:

    exists = conn.execute(
        text("SELECT id FROM users WHERE LOWER(email)=LOWER(:email)"),
        {"email": email}
    ).fetchone()

    if exists:

        conn.execute(
            text("""
            UPDATE users
            SET role='ADMIN',
                is_active=1,
                hashed_password=:hash
            WHERE LOWER(email)=LOWER(:email)
            """),
            {
                "hash": hashed,
                "email": email
            }
        )

        print("✅ تم تحديث حساب المشرف")

    else:

        conn.execute(
            text("""
            INSERT INTO users
            (full_name,email,hashed_password,role,is_active)
            VALUES
            (:name,:email,:hash,'ADMIN',1)
            """),
            {
                "name":"Aymen Mohamed",
                "email":email,
                "hash":hashed
            }
        )

        print("✅ تم إنشاء حساب المشرف")

print("Admin ready")

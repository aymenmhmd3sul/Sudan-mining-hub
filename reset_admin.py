import sqlite3
from passlib.context import CryptContext
from datetime import datetime, timezone

# استخدام نفس إعدادات السكيورتي الموحدة
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

conn = sqlite3.connect("local.db")
email = "aymen.mhmd3@gmail.com"
password = "realme50+fatman"

# إنتاج هاش مطابق تماماً للبيئة الحالية
password_hash = pwd_context.hash(password)
created_at = datetime.now(timezone.utc).isoformat()

# تحديث الهاش في الحساب الحالي بدقة
conn.execute("""
    UPDATE users 
    SET password_hash = ?, status = 'ACTIVE' 
    WHERE email = ?
""", (password_hash, email))

conn.commit()
conn.close()
print("🎯 ADMIN PASSWORD RESET SUCCESSFUL")

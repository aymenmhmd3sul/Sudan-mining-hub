import sqlite3
import os
from passlib.context import CryptContext
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "local.db")

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# إعادة إنشاء الجدول لضمان سلامة الهيكل والحقول 100%
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("""
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    status TEXT DEFAULT 'ACTIVE',
    created_at TEXT
);
""")

email = "aymen.mhmd3@gmail.com"
password = "realme50+fatman"
password_hash = pwd_context.hash(password)
created_at = datetime.now(timezone.utc).isoformat()

# حقن المستخدم بكافة الحقول المطلوبة للمنصة العالمية كمصدر وحيد للحقيقة
cursor.execute("""
INSERT INTO users (id, email, password_hash, role, is_active, status, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", ("usr_admin_001", email.strip(), password_hash, "superadmin", 1, "ACTIVE", created_at))

conn.commit()
conn.close()
print("🎯 DATABASE PURGED AND FRESH ADMIN SEEDED SUCCESSFULLY!")

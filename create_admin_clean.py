import sqlite3
from passlib.context import CryptContext
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

conn = sqlite3.connect("local.db")

email = "aymen.mhmd3@gmail.com"
password = "realme50+fatman"

password_hash = pwd_context.hash(password)
created_at = datetime.now(timezone.utc).isoformat()

conn.execute("""
INSERT INTO users (email, password_hash, role, status, created_at)
VALUES (?, ?, ?, ?, ?)
""", (email, password_hash, "superadmin", "ACTIVE", created_at))

conn.commit()
conn.close()

print("RESET ADMIN READY")

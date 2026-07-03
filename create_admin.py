import sqlite3
import crypt
from datetime import datetime, timezone

conn = sqlite3.connect("local.db")

email = "aymen.mhmd3@gmail.com"
password = "realme50+fatman"

password_hash = crypt.crypt(password)

conn.execute("""
INSERT INTO users (email, password_hash, role, status, created_at)
VALUES (?, ?, ?, ?, ?)
""", (
    email,
    password_hash,
    "superadmin",
    "ACTIVE",
    datetime.now(timezone.utc).isoformat()
))

conn.commit()
conn.close()

print("ADMIN FIXED WITH CRYPT")

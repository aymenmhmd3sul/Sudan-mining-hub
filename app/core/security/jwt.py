import jwt
from fastapi import HTTPException, Header
import sqlite3
import datetime

DB = "local.db"
SECRET_KEY = "YOUR_SECRET"
ALGORITHM = "HS256"

# ---------------- JWT CORE ----------------

def create_token(data: dict):
    payload = data.copy()
    payload.update({
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow()
    })
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------- DB ----------------

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- AUTH USER ----------------

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    conn = get_db()
    cur = conn.cursor()

    user = cur.execute(
        "SELECT id, name, email, role FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "id": user["id"],
        "email": user["email"],
        "role": user["role"]
    }

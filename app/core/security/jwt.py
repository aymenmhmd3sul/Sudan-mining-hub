import jwt
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, Header

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# =========================
# Create Token
# =========================
def create_token(data: dict):
    payload = data.copy()

    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["iat"] = datetime.utcnow()

    # expected payload: {"user_id": 1, "role": "buyer/seller/admin"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# =========================
# Decode Token
# =========================
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# =========================
# FastAPI Dependency (CORE SECURITY LAYER)
# =========================
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")

        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return payload

    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")


# =========================
# Role System
# =========================
def is_admin(user: dict) -> bool:
    return user.get("role") == "admin"


def require_admin(user: dict):
    if not is_admin(user):
        raise HTTPException(status_code=403, detail="Admin only")

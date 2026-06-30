import jwt
from fastapi import HTTPException
import datetime

SECRET_KEY = "super-secret-key-123456789"
ALGORITHM = "HS256"

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
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

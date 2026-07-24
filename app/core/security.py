from passlib.hash import pbkdf2_sha256
from types import SimpleNamespace
from datetime import datetime, timedelta, timezone
from jose import jwt
import os

settings = SimpleNamespace(
    SECRET_KEY=os.getenv("SECRET_KEY", "sudan-mining-hub-secret-key-2026"),
    ALGORITHM="HS256"
)

def get_password_hash(password: str) -> str:
    return pbkdf2_sha256.using(rounds=1000).hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

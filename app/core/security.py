import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_SUDAN_MINING_HUB_KEY_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# إزالة required=False لحل الـ TypeError تماماً
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# توفير الدالة القديمة والدالة الجديدة معاً لضمان عدم كسر أي ملفات أخرى في المشروع
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="جلسة غير صالحة أو منتهية، يرجى إعادة تسجيل الدخول",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception

async def get_current_admin(token: str = Depends(oauth2_scheme)):
    payload = await get_current_user(token)
    role: str = payload.get("role")
    email: str = payload.get("sub")
    if role != "admin" or email != "aymen.mhmd3@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="عذراً، لا تمتلك الصلاحيات الإدارية الكافية لدخول هذه المنصة"
        )
    return payload

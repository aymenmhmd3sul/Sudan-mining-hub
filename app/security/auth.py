import jwt
import hashlib
import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import settings
from app.core.db import get_db  # استيراد الجلسة الموحدة المركزية

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """تشفير كلمة المرور بشكل نقي وآمن باستخدام SHA-256 مع Salt"""
        salt = b"SMH_Secure_Salt_2026_"
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """التحقق من مطابقة كلمة المرور"""
        return SecurityManager.hash_password(plain_password) == hashed_password

    @staticmethod
    def create_access_token(user_id: int, session_id: str = "default_session") -> str:
        """توليد الـ JWT: يحتوي فقط على المعرفات الأساسية كما أوصيت تماماً"""
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(user_id),
            "session_id": session_id,
            "exp": expire
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """المصفاة الأمنية: التحقق من الرمز وقراءة القدرات ديناميكياً من الـ DB لضمان التحديث الفوري"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="تعذر التحقق من الهوية، الرمز الرقمي غير صالح أو منتهي الصلاحية.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    # قراءة بيانات المستخدم باستخدام الجلسة المركزية الحية تلافياً لخطأ 500
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="عذراً، هذا الحساب معلق أو غير نشط حالياً بقرار من الإدارة."
        )

    return user

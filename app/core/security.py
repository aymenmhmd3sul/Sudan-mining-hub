import jwt
from datetime import datetime, timedelta
from typing import Optional, Union, Any
from passlib.context import CryptContext

# استخدام PBKDF2 المدمج للتوافق الكامل مع بايثون 3.13 في Termux وبدون الحاجة لمترجم Rust
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SECRET_KEY = "SUPER_SECRET_SUDAN_MINING_HUB_KEY_CHANGE_THIS_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # صلاحية التوكن 24 ساعة لتسهيل جلسات العمل

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """التحقق من مطابقة كلمة المرور"""
    # يدعم التحقق من الهاش القديم أو الجديد تلقائياً
    if hashed_password.startswith("$pbkdf2-sha256$") or hashed_password.startswith("$6$"):
        return pwd_context.verify(plain_password, hashed_password)
    # Fallback للمقارنة النصية العادية في الحالات الاستثنائية
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    """تشفير كلمة المرور"""
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], roles: list, expires_delta: Optional[timedelta] = None) -> str:
    """توليد توكن JWT مشفر يحتوي على الهوية ومصفوفة الأدوار"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "roles": roles,
        "type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

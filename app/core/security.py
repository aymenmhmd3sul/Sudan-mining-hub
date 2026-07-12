import bcrypt
from datetime import datetime, timedelta
from typing import Any, Union
import jwt
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "SUPER_SECRET_MINING_HUB_KEY_2026_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # أسبوع كامل للمستكشفين والوكلاء

    # هنا الحل الجذري: نطلب من Pydantic تجاهل أي متغيرات بيئة إضافية في ريندر وعدم قفل السيرفر بسببها
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()

def get_password_hash(password: str) -> str:
    """توليد هاش آمن للمستقبل باستخدام الكود الأصيل لحزمة bcrypt"""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """التحقق الآمن والأبدي من كلمات المرور دون الاعتماد على مكتبات وسيطة تنهار في البيئات الحية"""
    try:
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """توليد توكنات الدخول واعتماد الحالات الحية للمنظومة"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

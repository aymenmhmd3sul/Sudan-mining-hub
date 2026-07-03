import jwt
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# إعدادات الأمان الأساسية للمنصة العالمية
SECRET_KEY = "SUDAN_MINING_HUB_SECURE_PRODUCTION_KEY_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# جعل pbkdf2_sha256 الخوارزمية الأولى لتطابق الهاش الحي في قاعدة البيانات فورا
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # استخراج البيانات الهيكلية الكاملة لتوحيد الصلاحيات في المنصة
        user_id: str = payload.get("id")
        email: str = payload.get("sub")
        role: str = payload.get("role")
        is_active: bool = payload.get("is_active", True)
        status_user: str = payload.get("status", "ACTIVE")
        
        if email is None or user_id is None:
            raise credentials_exception
            
        # منع الحسابات المعطلة أو المحظورة فوراً من العبور لأي Endpoint
        if not is_active or status_user in ["SUSPENDED", "REJECTED"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is inactive or suspended"
            )
            
        return {
            "id": user_id,
            "email": email,
            "role": role,
            "is_active": is_active,
            "status": status_user
        }
    except jwt.PyJWTError:
        raise credentials_exception

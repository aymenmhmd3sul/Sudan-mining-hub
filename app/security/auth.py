import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import settings, create_access_token # استيراد الدالة الموحدة
from app.core.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """المصفاة الأمنية: التحقق الموحد باستخدام الإعدادات المركزية"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="تعذر التحقق من الهوية، الرمز الرقمي غير صالح أو منتهي الصلاحية.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # فك التشفير باستخدام الإعدادات الموحدة
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="عذراً، هذا الحساب معلق."
        )
    return user

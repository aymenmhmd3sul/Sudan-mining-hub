import os
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import jwt
from app.database import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM

# --- الاعتمادية المركزية: استخراج المستخدم من الـ Cookie أو الـ Authorization Header ---
async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        # محاولة فحص الـ Header إذا لم يوجد كوكي (لدعم الـ APIs النقية)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="غير مسجل دخول - التوكن مفقود")

    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="توكن غير صالح")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="انتهت صلاحية الجلسة")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="المستخدم غير موجود")
    return user

class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="الحساب غير نشط أو تم تجميده أمنياً"
            )

        if self.required_permission and self.required_permission not in user.permissions_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"عذراً، لا تمتلك الصلاحية التشغيلية: [{self.required_permission}]"
            )

        return user

# --- جسور التوافقية الرجعية للموجهات القديمة ---
def require_any_user(user: User = Depends(get_current_user)) -> dict:
    return {"id": user.id, "email": user.email, "full_name": user.full_name}

def require_seller(user: User = Depends(get_current_user)) -> dict:
    return {"id": user.id, "email": user.email, "full_name": user.full_name}

def require_buyer(user: User = Depends(get_current_user)) -> dict:
    return {"id": user.id, "email": user.email, "full_name": user.full_name}

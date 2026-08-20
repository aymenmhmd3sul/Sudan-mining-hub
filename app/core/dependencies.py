from fastapi import Depends, HTTPException, status
from app.security.auth import get_current_user
from app.models.auth import User, UserRole


def _require_active(current_user: User) -> User:
    if not current_user or not getattr(current_user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="جلسة عمل غير صالحة، يرجى تسجيل الدخول",
        )
    return current_user


def verify_admin_token(current_user: User = Depends(get_current_user)):
    current_user = _require_active(current_user)
    role = str(getattr(current_user.role, "value", current_user.role)).lower()

    if role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول: يتطلب صلاحيات مدير",
        )
    return current_user


def require_any_user(current_user: User = Depends(get_current_user)):
    return _require_active(current_user)


def require_merchant(current_user: User = Depends(get_current_user)):
    current_user = _require_active(current_user)
    role = str(getattr(current_user.role, "value", current_user.role)).lower()

    if role != UserRole.MERCHANT.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول إلى لوحة التاجر",
        )
    return current_user


def require_buyer(current_user: User = Depends(get_current_user)):
    current_user = _require_active(current_user)
    role = str(getattr(current_user.role, "value", current_user.role)).lower()

    if role != UserRole.BUYER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول إلى لوحة المشتري",
        )
    return current_user


def require_agent(current_user: User = Depends(get_current_user)):
    current_user = _require_active(current_user)
    role = str(getattr(current_user.role, "value", current_user.role)).lower()

    if role != UserRole.AGENT.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول إلى لوحة الوكيل",
        )
    return current_user


def require_seller(current_user: User = Depends(get_current_user)):
    current_user = _require_active(current_user)
    role = str(getattr(current_user.role, "value", current_user.role)).lower()

    if role not in {UserRole.MERCHANT.value, "seller"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول إلى مساحة التاجر",
        )
    return current_user

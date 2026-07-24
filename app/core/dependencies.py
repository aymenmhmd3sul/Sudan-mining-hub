from fastapi import Depends, HTTPException, status
from app.security.auth import get_current_user
from app.models.auth import User, UserRole

def verify_admin_token(current_user: User = Depends(get_current_user)):
    role = getattr(current_user.role, 'value', current_user.role)
    is_admin = str(role).lower() == UserRole.ADMIN.value.lower()
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول: يتطلب صلاحيات مدير"
        )
    return current_user

def require_seller(current_user: User = Depends(get_current_user)):
    if not current_user or not getattr(current_user, 'is_active', True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="جلسة العمل غير صالحة أو الحساب غير نشط"
        )
    
    user_dict = {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name
    }
    return user_dict

def require_any_user(current_user: User = Depends(get_current_user)):
    """
    التحقق من وجود مستخدم نشط بالنظام (أياً كان نوع حسابه)
    وتمرير بياناته كـ dict لتلبية نداء current_user["id"]
    """
    if not current_user or not getattr(current_user, 'is_active', True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="جلسة عمل غير صالحة، يرجى تسجيل الدخول"
        )
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name
    }

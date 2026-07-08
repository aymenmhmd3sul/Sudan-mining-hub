from fastapi import Depends, HTTPException
from app.security.auth import get_current_user
from app.models.user import User

def verify_admin_token(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, 
            detail="غير مصرح لك بالوصول: يتطلب صلاحيات مدير"
        )
    return current_user

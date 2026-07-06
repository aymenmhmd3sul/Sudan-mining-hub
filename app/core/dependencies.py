from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user
from app.models.user import User
from sqlalchemy.orm import Session
from app.core.db import get_db

class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, payload: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="الحساب غير موجود أو تم تجميده أمنياً"
            )
            
        if self.required_permission not in user.permissions_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"عذراً، لا تمتلك الصلاحية التشغيلية للمنصة: [{self.required_permission}]"
            )
            
        return user

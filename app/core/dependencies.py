from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"غير مصرح لك بإجراء هذه العملية. الصلاحيات المطلوبة: {self.allowed_roles}"
            )
        return current_user

# تعريف الصلاحيات الجاهزة للاستخدام في الـ Routers
require_admin = RoleChecker(["superadmin"])
require_seller = RoleChecker(["superadmin", "seller"])
require_buyer = RoleChecker(["superadmin", "buyer"])
require_any_user = RoleChecker(["superadmin", "seller", "buyer"])

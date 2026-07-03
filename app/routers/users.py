from fastapi import APIRouter, Depends
from app.core.security import get_current_user

# توحيد البادئة البرمجية للراوتر لضمان الاتساق الهيكلي
router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """
    نقطة النهاية الموحدة لاسترجاع بيانات المستخدم الحالي الموثق.
    تعتمد كلياً على الحمولة الشاملة القادمة من التوكن لضمان السرعة والأمن.
    """
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "role": current_user["role"],
        "is_active": current_user["is_active"],
        "status": current_user["status"]
    }

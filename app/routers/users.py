from fastapi import APIRouter, Depends
from app.security.auth import get_current_user
from app.models.auth import User

# توحيد البادئة البرمجية للراوتر لضمان الاتساق الهيكلي
router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/profile")
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    نقطة النهاية الموحدة لاسترجاع بيانات الهوية الحية للمستخدم الحالي الموثق
    مباشرة من كائن الـ ORM الموحد والمحمي.
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "role": current_user.role.value,
        "status": current_user.status.value,
        "country": current_user.country,
        "language": current_user.language
    }

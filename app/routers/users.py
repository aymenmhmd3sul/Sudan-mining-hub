from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me")
def get_my_profile(current_user: dict = Depends(get_current_user)):
    user_profile = UserService.get_user_by_email(current_user["email"])
    return user_profile

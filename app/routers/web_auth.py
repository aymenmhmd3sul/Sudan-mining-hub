from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/web", tags=["Web Auth"])


@router.post("/login")
def web_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    result = AuthService.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    return {
        "redirect": "/admin/dashboard",
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "message": "تم تسجيل الدخول بنجاح"
    }

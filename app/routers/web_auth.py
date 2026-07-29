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

    user = result.get("user")

    if user:
        role = user.role if hasattr(user, "role") else user.get("role")
    else:
        role = None

    role = str(role).upper() if role else ""

    if role == "ADMIN":
        redirect = "/admin/dashboard"
    elif role == "MERCHANT":
        redirect = "/merchant"
    elif role == "AGENT":
        redirect = "/agent"
    elif role == "BUYER":
        redirect = "/dashboard"
    else:
        redirect = "/visitor"

    return {
        "redirect": redirect,
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "message": "تم تسجيل الدخول بنجاح"
    }

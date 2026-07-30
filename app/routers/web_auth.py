from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/web", tags=["Web Auth"])


@router.post("/login")
def web_login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    result = AuthService.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )


    user = result.get("user", {})


    role = user.get("role", "") if isinstance(user, dict) else ""

    role = str(role).upper()

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

    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        max_age=3600,
        samesite="lax"
    )

    return {
        "redirect": redirect,
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "message": "تم تسجيل الدخول بنجاح"
    }

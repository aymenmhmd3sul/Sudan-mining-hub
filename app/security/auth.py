from jose import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from app.models.auth import User
from app.core.security import settings
from app.core.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    try:
        if not token:
            token = request.cookies.get("access_token")

        if token and token.startswith("Bearer "):
            token = token.replace("Bearer ", "", 1)

        if not token:
            raise Exception("Missing authentication token")

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        
        user = db.query(User).filter(
            User.email == email
        ).first()

        # حساب المشرف الأساسي للنظام
        if not user and email in ["aymen.mhmd3@gmail.com", "admin@sudanmining.com"]:
            return type("AdminUser", (), {
                "id": 1,
                "email": email,
                "role": "ADMIN",
                "is_active": True,
                "status": "ACTIVE",
                "name": "AYMEN ADMIN"
            })()

        if not user:
            raise Exception("User not found")

        if not user.is_active:
            raise Exception("Inactive user")
            
        return user
    except Exception as e:
        print("AUTH_ERROR:", repr(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

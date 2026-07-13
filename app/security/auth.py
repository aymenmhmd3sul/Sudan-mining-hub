import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.core.security import settings
from app.core.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        
        user = db.query(User).options(joinedload(User.roles)).filter(User.id == int(user_id)).first()
        
        if not user:
            raise Exception("User not found")
        
        if not user.is_active:
            raise Exception("Inactive user")
            
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="تعذر التحقق من الهوية أو الصلاحيات."
        )

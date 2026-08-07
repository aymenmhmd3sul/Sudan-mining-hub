from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter()


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    existing = db.query(User).filter(
        (User.email == user.email) |
        (User.phone == user.phone)
    ).first()

    if existing:
        if existing.email == user.email:
            detail = "البريد الإلكتروني مسجل مسبقاً"
        else:
            detail = "رقم الهاتف مسجل مسبقاً"

        raise HTTPException(
            status_code=400,
            detail=detail
        )

    new_user = User(
        name=user.name,
        full_name=user.name,
        email=user.email,
        phone=user.phone,
        hashed_password=get_password_hash(user.password),
        password_hash=get_password_hash(user.password),
        role=user.role,
        status="ACTIVE"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax"
    )

    return {
        "status": "success",
        "user_id": new_user.id
    }


@router.post("/login")
def login(
    user: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="البريد أو كلمة المرور غير صحيحة"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="البريد أو كلمة المرور غير صحيحة"
        )

    token = create_access_token(
        {
            "sub": db_user.email,
            "role": str(db_user.role)
        }
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax"
    )

    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "role": db_user.role,
            "is_admin": db_user.is_admin
        }
    }

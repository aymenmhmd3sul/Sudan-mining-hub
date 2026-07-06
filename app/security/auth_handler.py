from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(email: str = "aymen.mhmd3@gmail.com", db: Session = Depends(get_db)):
    """تابع افتراضي لجلب المستخدم الحالي بناءً على البريد المحقون إدارياً لحين ربط الـ JWT"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="مستخدم غير مسجل أو منتهي الصلاحية."
        )
    return user

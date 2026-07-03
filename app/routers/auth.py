from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.core.db import get_db_connection
from app.core.security import verify_password, create_access_token

router = APIRouter(tags=["Authentication"])

# 📦 الموديل لاستقبال البيانات كـ JSON نظيف بدون تشويه المحارف
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(payload: LoginRequest):
    """تسجيل الدخول الآمن باستخدام JSON Payload لحماية الإيميلات الخاصة."""
    user_email = payload.email.strip()
    password = payload.password

    conn = get_db_connection()
    # ⚠️ تعديل المسمى هنا إلى password_hash ليتطابق مع قاعدة البيانات
    user = conn.execute(
        "SELECT id, email, password_hash, role, is_active, status FROM users WHERE email = ?", 
        (user_email,)
    ).fetchone()
    conn.close()

    # التحقق من وجود المستخدم وصحة كلمة المرور باستخدام الحقل الصحيح
    if not user or not verify_password(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="بيانات الدخول غير صحيحة، تأكد من الإيميل وكلمة المرور"
        )

    # إنشاء التوكن الموحد لعام 2026 متضمناً كامل البيانات الهيكلية
    token_data = {
        "id": user["id"],
        "sub": user["email"],
        "role": user["role"],
        "is_active": bool(user["is_active"]),
        "status": user["status"]
    }
    
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"]
        }
    }

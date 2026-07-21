from fastapi.responses import JSONResponse, Response
from fastapi import Request, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

# الاستيرادات الدقيقة والمحققة من بنية المشروع الحالية
from app.core.db import get_db
from app.security.auth import get_current_user
from app.core.security import get_password_hash
from app.models.auth import User, UserRole, UserStatus
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Identity & Trust"])

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    country: Optional[str] = "SD"
    language: Optional[str] = "ar"

class RoleUpgradeRequest(BaseModel):
    requested_role: UserRole

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """إنشاء الهوية الموحدة والآمنة في النظام"""
    existing_email = db.query(User).filter(User.email == user_data.email.strip().lower()).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني مسجل بالفعل في النظام."
        )

    existing_phone = db.query(User).filter(User.phone == user_data.phone.strip()).first()
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رقم الهاتف مسجل بالفعل في النظام."
        )

    # استخدام الاسم الصحيح والمحقق للدالة هنا
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name.strip(),
        email=user_data.email.strip().lower(),
        phone=user_data.phone.strip(),
        password_hash=hashed_pwd,
        role=UserRole.BUYER,
        status=UserStatus.PENDING,
        country=user_data.country,
        language=user_data.language
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "✅ تم إنشاء حسابك الموحد بنجاح! حسابك الآن في انتظار مراجعة الإدارة والاعتماد الفوري."}

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    # محاولة قراءة البيانات سواء كانت JSON أو Form Data
    email = None
    password = None
    
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            body = await request.json()
            email = body.get("email") or body.get("username")
            password = body.get("password")
        except Exception:
            pass
    
    if not email or not password:
        try:
            form = await request.form()
            email = form.get("username") or form.get("email")
            password = form.get("password")
        except Exception:
            pass

    if not email or not password:
        return JSONResponse(status_code=400, content={"detail": "يرجى إدخال البريد الإلكتروني وكلمة المرور"})

    email = email.strip().lower()

    # 1. فحص الحساب الثابت للمشرف
    if (email == "aymen.mhmd3@gmail.com" or email == "admin@sudanmining.com") and password == "SudanMining@2026":
        access_token = "admin_secure_access_token"
        response = JSONResponse(content={"status": "success", "message": "تم الدخول بنجاح", "redirect": "/admin"})
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=2592000, # 30 يوماً
            samesite="lax"
        )
        return response

    # 2. فحص الحسابات من قاعدة البيانات
    user = db.query(User).filter(User.email == email).first() if 'User' in globals() or 'User' in locals() else None
    if user and verify_password(password, user.password_hash):
        access_token = create_access_token(data={"sub": user.email})
        response = JSONResponse(content={"status": "success", "message": "تم الدخول بنجاح", "redirect": "/admin"})
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=2592000,
            samesite="lax"
        )
        return response

    return JSONResponse(status_code=401, content={"detail": "خطأ في البريد الإلكتروني أو كلمة المرور"})
@router.post("/request-role")
def request_role_upgrade(req: RoleUpgradeRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """طلب تعديل الصلاحيات أو الترقية لأدوار حيوية كـ MERCHANT أو AGENT"""
    if req.requested_role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="لا يمكن طلب صلاحيات مدير النظام يدوياً."
        )
    
    current_user.role = req.requested_role
    db.commit()
    return {"message": f"✅ تم الانتقال إلى دور ({req.requested_role.value}) بنجاح."}

@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    """استعراض ملف المستخدم الحي مباشرة من كائن الـ ORM المستقر"""
    return {
        "id": current_user.id,
        "name": getattr(current_user, "name", getattr(current_user, "full_name", "Admin")),
        "email": current_user.email,
        "phone": current_user.phone,
        "role": getattr(current_user.role, "value", current_user.role),
        "status": getattr(current_user.status, "value", current_user.status),
        "country": current_user.country,
        "language": current_user.language
    }

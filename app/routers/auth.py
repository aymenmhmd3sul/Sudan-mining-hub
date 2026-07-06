from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.security.auth import SecurityManager, get_db, get_current_user
from app.models.identity import User
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Identity & Trust"])

# نماذج التحقق من البيانات المدخلة (Schemas)
class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone_number: str = None

class CapabilityRequest(BaseModel):
    capability: str # 'seller', 'importer', 'global_provider'

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """المرحلة الأولى: إنشاء الهوية الموحدة في النظام"""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني مسجل بالفعل في النظام."
        )
    
    hashed_pwd = SecurityManager.hash_password(user_data.password)
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_pwd,
        phone_number=user_data.phone_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "✅ تم إنشاء حسابك الموحد بنجاح! يمكنك الآن تسجيل الدخول وتفعيل القدرات."}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """تسجيل الدخول وتوليد رمز JWT خفيف يحتوي على المعرفات فقط"""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not SecurityManager.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة."
        )
    
    token = SecurityManager.create_access_token(user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/activate-capability")
def activate_user_capability(req: CapabilityRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """المرحلة الثالثة: تفعيل القدرات بشكل متدرج وديناميكي داخل الحساب الموحد"""
    cap = req.capability.lower()
    
    if cap == "seller":
        current_user.is_seller = True
        msg = "تم تفعيل قدرة (تاجر/معدن) تلقائياً، يمكنك الآن نشر الأصول."
    elif cap == "importer":
        current_user.is_importer = True
        msg = "تم تفعيل قدرة (مستورد) تلقائياً، يمكنك الآن استخدام Global Trade Desk."
    elif cap == "global_provider":
        # القدرات الحساسة تتطلب مراجعة واعتماد الإدارة كما أوصيت تماماً
        current_user.is_global_provider = True 
        current_user.is_verified_by_admin = False # ينتظر مراجعة مستنداته من قبلك
        msg = "تم رفع طلب الاعتماد كمزود خدمات عالمي (Global Service Provider)، في انتظار مراجعة الإدارة للمستندات."
    else:
        raise HTTPException(status_code=400, detail="نوع القدرة المطلوبة غير مدعوم.")
        
    db.commit()
    return {"message": f"✅ {msg}"}

@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    """المرحلة الثانية: استعراض بيانات الملف الشخصي والقدرات النشطة حالياً حيةً من الـ DB"""
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone_number": current_user.phone_number,
        "capabilities": {
            "is_admin": current_user.is_admin,
            "is_moderator": current_user.is_moderator,
            "is_seller": current_user.is_seller,
            "is_importer": current_user.is_importer,
            "is_global_provider": current_user.is_global_provider
        },
        "is_verified": current_user.is_verified_by_admin
    }

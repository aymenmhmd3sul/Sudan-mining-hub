from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import sqlalchemy as sa
from app.models.auth import User, UserStatus
from app.core.security import verify_password, create_access_token

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> dict:
        # تطهير المدخلات فوراً من أي فراغات زائدة وتحويلها لأحرف صغيرة
        clean_username = username.strip().lower()
        
        # استعلام ORM قياسي وصريح ومحمي
        user = db.query(User).filter(sa.func.lower(User.email) == clean_username).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="البريد الإلكتروني أو كلمة المرور غير صحيحة."
            )
            
        # التحقق من كلمة المرور باستخدام الـ Hash المخزن
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="البريد الإلكتروني أو كلمة المرور غير صحيحة."
            )
            
        # استخراج القيمة النصية للحالة لضمان استقرار المقارنة
        current_status = user.status.value if hasattr(user.status, 'value') else user.status
        
        # التحقق الصارم من حالة الحساب بناءً على الحالات الأربعة
        if current_status == UserStatus.SUSPENDED.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="تم تعليق حسابك. يرجى مراجعة الدعم الفني."
            )
        elif current_status == UserStatus.PENDING.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="حسابك في انتظار مراجعة الإدارة والموافقة."
            )
        elif current_status == UserStatus.REJECTED.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="تم رفض طلب انضمامك إلى المنصة."
            )

        # تجهيز بيانات التوكن (Token Claims) من كائن الـ ORM مباشرة
        token_data = {
            "id": user.id,
            "sub": user.email,
            "role": user.role.value if hasattr(user.role, 'value') else user.role,
            "status": current_status
        }
        
        token = create_access_token(data=token_data)
        return {
            "access_token": token,
            "token_type": "bearer"
        }

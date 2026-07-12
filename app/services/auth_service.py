from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.auth import User, UserStatus
from app.core.security import verify_password, create_access_token

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> dict:
        # تطهير المدخلات فوراً من أي فراغات زائدة وتحويلها لأحرف صغيرة
        clean_username = username.strip().lower()

        # الاستعلام باستخدام الـ ORM والمقارنة الآمنة والمفهرسة
        user = db.query(User).filter(sa.func.lower(User.email) == clean_username).first() if 'sa' in globals() else db.query(User).filter(User.email == clean_username).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # التحقق من كلمة المرور باستخدام الـ Hash المخزن صراحة في الموديل الجديد
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # التحقق الصارم من حالة الحساب بناءً على الحالات الأربعة المعتمدة
        if user.status == UserStatus.SUSPENDED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been suspended. Please contact support."
            )
        elif user.status == UserStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account registration is pending approval."
            )
        elif user.status == UserStatus.REJECTED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account application has been rejected."
            )

        # تجهيز بيانات التوكن (Token Claims) من كائن الـ ORM مباشرة وثابت البيانات
        token_data = {
            "id": user.id,
            "sub": user.email,
            "role": user.role.value,
            "status": user.status.value
        }

        token = create_access_token(data=token_data)

        return {
            "access_token": token,
            "token_type": "bearer"
        }

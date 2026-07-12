from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.auth import User, UserRole, UserStatus

class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        user = db.query(User).filter(User.email == email.strip()).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    def update_user_role(db: Session, email: str, new_role: str) -> dict:
        # الأدوار المسموحة الصارمة (بدون visitor)
        allowed_roles = [role.value for role in UserRole]
        if new_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role must be one of {allowed_roles}"
            )

        user = db.query(User).filter(User.email == email.strip()).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found to update role"
            )

        user.role = UserRole(new_role)
        db.commit()
        db.refresh(user)
        
        return {"status": "success", "message": f"User role updated to {new_role}"}

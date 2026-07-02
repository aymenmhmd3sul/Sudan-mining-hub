from fastapi import HTTPException, status
from app.core.db import get_db_connection

class UserService:
    @staticmethod
    def get_user_by_email(email: str) -> dict:
        conn = get_db_connection()
        user_row = conn.execute(
            "SELECT id, email, role, is_active FROM users WHERE email = ?",
            (email.strip(),)
        ).fetchone()
        conn.close()
        
        if not user_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return dict(user_row)

    @staticmethod
    def update_user_role(email: str, new_role: str) -> dict:
        # إضافة دور visitor إلى الأدوار المسموحة في النظام
        allowed_roles = ["admin", "seller", "buyer", "visitor"]
        if new_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role must be one of {allowed_roles}"
            )
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET role = ? WHERE email = ?",
            (new_role, email.strip())
        )
        conn.commit()
        changes = cursor.rowcount
        conn.close()
        
        if changes == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found to update role"
            )
            
        return {"status": "success", "message": f"User role updated to {new_role}"}

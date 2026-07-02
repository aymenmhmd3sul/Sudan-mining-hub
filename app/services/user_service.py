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

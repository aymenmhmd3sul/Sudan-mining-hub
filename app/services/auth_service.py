from fastapi import HTTPException, status
from app.core.db import get_db_connection
from app.core.security import verify_password, create_access_token

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> dict:
        # تطهير المدخلات فوراً من أي فراغات زائدة وتحويلها لأحرف صغيرة
        clean_username = username.strip().lower()
        
        conn = get_db_connection()
        # استخدام LOWER في الاستعلام لضمان التطابق التام بغض النظر عن طريقة الحفظ
        user_row = conn.execute(
            "SELECT * FROM users WHERE LOWER(TRIM(email)) = ?",
            (clean_username,)
        ).fetchone()
        conn.close()

        if not user_row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials"
            )
        
        user = dict(user_row)
        stored_hash = user.get("password_hash") or user.get("password")

        if not stored_hash or not verify_password(password, stored_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials"
            )

        user_id = str(user.get("id")) if user.get("id") else f"usr_{user['email'].split('@')[0]}"
        is_active = bool(user.get("is_active")) if "is_active" in user else True
        user_status = user.get("status", "ACTIVE").upper()

        token_data = {
            "id": user_id,
            "sub": user["email"].strip().lower(),
            "role": user["role"],
            "is_active": is_active,
            "status": user_status
        }
        
        token = create_access_token(data=token_data)
        
        return {
            "access_token": token,
            "token_type": "bearer"
        }

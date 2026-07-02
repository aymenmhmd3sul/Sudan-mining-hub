from fastapi import HTTPException
from app.core.db import get_db_connection
from app.core.security import verify_password, create_access_token

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> dict:
        conn = get_db_connection()
        user_row = conn.execute(
            "SELECT * FROM users WHERE email = ?", 
            (username.strip(),)
        ).fetchone()
        conn.close()
        
        if not user_row:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        user = dict(user_row)
        stored_hash = user.get("password_hash")
        
        if not stored_hash or not verify_password(password, stored_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        token_data = {
            "sub": user["email"],
            "role": user["role"]
        }
        token = create_access_token(data=token_data)
        
        return {
            "access_token": token,
            "token_type": "bearer"
        }

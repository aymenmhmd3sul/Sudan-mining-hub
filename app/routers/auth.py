from fastapi import APIRouter, HTTPException, Form, Header
from app.core.db import get_db
from app.core.security.jwt import create_token, decode_token
from passlib.hash import sha256_crypt

router = APIRouter(prefix="/api/auth", tags=["auth"])

# ---------------- LOGIN ----------------
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    try:
        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (username,)
        ).fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # safe password verification
        try:
            if not sha256_crypt.verify(password, user["password_hash"]):
                raise HTTPException(status_code=401, detail="Invalid credentials")
        except Exception:
            raise HTTPException(status_code=500, detail="Password verification failed")

        token = create_token({
            "sub": user["email"],
            "role": user["role"]
        })

        return {
            "message": "login successful",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "email": user["email"],
                "role": user["role"]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- ME ----------------
@router.get("/me")
def me(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)

    return {
        "email": payload["sub"],
        "role": payload["role"]
    }


# ---------------- LOGOUT ----------------
@router.post("/logout")
def logout():
    return {"message": "logged out"}

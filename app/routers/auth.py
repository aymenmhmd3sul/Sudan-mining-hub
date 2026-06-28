from fastapi import APIRouter, Depends, HTTPException, Header, Form
from app.core.security.jwt import create_token, decode_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ---------------- LOGIN ----------------
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):

    # مؤقتاً (حسب نظامك الحالي في sqlite)
    from app.core.db import get_db
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE email = ? AND password_hash = ?",
        (username, password)
    ).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": user["email"],
        "role": user["role"]
    })

    return {
        "message": "login successful",
        "user": {
            "email": user["email"],
            "role": user["role"]
        },
        "access_token": token
    }


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

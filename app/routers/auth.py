from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import json
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key-123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

router = APIRouter()

# ✅ تم التحديث هنا: دعم كلاً من scrypt (للمستخدمين الحاليين) و bcrypt (للمستخدمين الجدد)
pwd_context = CryptContext(schemes=["scrypt", "bcrypt"], deprecated="auto")
USERS_FILE = "data/users.json"

def get_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def get_user_by_email(email: str):
    users = get_users()
    for u in users:
        if u["email"] == email:
            return u
    return None

def verify_password(plain_password, hashed_password):
    try:
        # ✅ تمت إضافة try/except لضمان عدم حدوث خطأ 500 إذا فشلت عملية التحقق
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        if email is None or role is None:
            return None
        return {"email": email, "role": role}
    except JWTError:
        return None

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    from app.main import templates
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user["email"], "role": user["role"]})
    
    if "text/html" in request.headers.get("accept", ""):
        if user["role"] == "admin":
            response = RedirectResponse(url="/admin/", status_code=303)
        elif user["role"] == "seller":
            response = RedirectResponse(url="/seller/", status_code=303)
        else:
            response = RedirectResponse(url="/buyer/", status_code=303)
        
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response

    return {"access_token": access_token, "token_type": "bearer", "user": {"email": user["email"], "role": user["role"]}}

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie("access_token")
    return response

@router.get("/me")
def read_users_me(token: str = Depends()):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return current_user

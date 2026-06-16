from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import json
import os
from datetime import datetime, timedelta

router = APIRouter()
USERS_FILE = "data/users.json"

# التأكد من وجود ملف المستخدمين
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

class UserRegister(BaseModel):
    name: str
    email: str
    phone: str
    role: str  # buyer, seller, admin
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def get_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

@router.post("/register")
def register(user: UserRegister):
    users = get_users()
    
    # التحقق من أن البريد غير مستخدم
    for u in users:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجل مسبقاً")
    
    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "password": user.password,  # في المستقبل: تشفير
        "is_active": False if user.role == "seller" else True,  # التاجر يحتاج تفعيل
        "subscription_end": None,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    users.append(new_user)
    save_users(users)
    return {"status": "success", "message": "تم التسجيل بنجاح", "user_id": new_user["id"]}

@router.post("/login")
def login(user: UserLogin):
    users = get_users()
    for u in users:
        if u["email"] == user.email and u["password"] == user.password:
            return {
                "status": "success",
                "user": {
                    "id": u["id"],
                    "name": u["name"],
                    "email": u["email"],
                    "role": u["role"],
                    "is_active": u.get("is_active", False)
                }
            }
    raise HTTPException(status_code=401, detail="البريد أو كلمة المرور غير صحيحة")

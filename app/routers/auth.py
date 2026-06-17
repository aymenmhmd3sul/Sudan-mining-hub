from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import json
import os
from datetime import datetime, timedelta

router = APIRouter()
USERS_FILE = "data/users.json"

# التأكد من وجود مجلد data
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

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

# ============================================================
# دالة البذور (Seed) لإنشاء الحسابات الثابتة تلقائياً
# ============================================================
def seed_default_users():
    users = get_users()
    updated = False

    # 1. التأكد من وجود المشتري (أحمد)
    ahmed_exists = any(u["email"] == "ahmed@test.com" for u in users)
    if not ahmed_exists:
        users.append({
            "id": len(users) + 1,
            "name": "أحمد المشتري",
            "email": "ahmed@test.com",
            "phone": "0911111111",
            "role": "buyer",
            "password": "123456",
            "is_active": True,
            "subscription_end": None,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        updated = True
        print("✅ تم إنشاء حساب المشتري (أحمد) تلقائياً.")

    # 2. التأكد من وجود التاجر (التاجر التجريبي)
    trader_exists = any(u["email"] == "trader@test.com" for u in users)
    if not trader_exists:
        users.append({
            "id": len(users) + 1,
            "name": "تاجر تجريبي",
            "email": "trader@test.com",
            "phone": "0922222222",
            "role": "seller",
            "password": "123456",
            "is_active": True,  # مُفعل تلقائياً
            "subscription_end": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        updated = True
        print("✅ تم إنشاء حساب التاجر (التاجر التجريبي) تلقائياً مع تفعيل الاشتراك.")

    # 3. إذا كان التاجر موجوداً ولكن غير نشط، نفعله
    for u in users:
        if u["email"] == "trader@test.com" and u.get("is_active") is False:
            u["is_active"] = True
            u["subscription_end"] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
            updated = True
            print("✅ تم تفعيل حساب التاجر (التاجر التجريبي) تلقائياً.")

    if updated:
        save_users(users)

# استدعاء دالة البذور عند بدء تشغيل الروتر
seed_default_users()

# ============================================================
# نقاط النهاية (Endpoints)
# ============================================================
@router.post("/register")
def register(user: UserRegister):
    users = get_users()
    for u in users:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجل مسبقاً")
    
    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "password": user.password,
        "is_active": False if user.role == "seller" else True,
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

from fastapi import APIRouter, HTTPException, Request
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime, timedelta

router = APIRouter()

USERS_FILE = "data/users.json"

def get_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def is_werkzeug_hash(password: str) -> bool:
    return (
        password.startswith('pbkdf2:sha256:') or
        password.startswith('scrypt:') or
        password.startswith('argon2:')
    )

@router.post("/login")
async def login(request: Request):
    data = await request.json()

    email = data.get("email")
    password = data.get("password")

    users = get_users()

    for u in users:
        if u["email"] == email:

            stored_password = u["password"]

            if check_password_hash(stored_password, password):
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

    raise HTTPException(status_code=401, detail="البريد أو كلمة المرور غير صحيحة")

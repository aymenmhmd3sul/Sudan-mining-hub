import hashlib, secrets
from fastapi import Request

users_db = {
    "admin@test.com": {"name": "مدير النظام", "password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "admin"}
}
sessions = {}

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def create_session(email):
    token = secrets.token_urlsafe(32)
    sessions[token] = email
    return token

def get_user(email):
    return users_db.get(email)

def get_user_from_cookie(request: Request):
    token = request.cookies.get("session_token")
    if not token or token not in sessions:
        return None
    email = sessions[token]
    return users_db.get(email)

async def get_gold_price():
    import httpx
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get("https://api.gold-api.com/price/XAU")
            if r.status_code == 200:
                return r.json().get("price", 4315.09)
            return 4315.09
    except:
        return 4315.09

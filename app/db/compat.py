# =========================
# SIMPLE RUNTIME MEMORY DB
# =========================

DB = {
    "users": {},
    "gold": 0
}


# USERS
def users_db():
    return DB["users"]


def add_user(user_id: str, email: str, password: str, role: str = "user"):
    DB["users"][user_id] = {
        "email": email,
        "password": password,
        "role": role
    }


# AUTH HELPERS
def get_user_from_cookie(token: str):
    return None


# GOLD (placeholder)
def get_gold_price():
    return {"gold": DB["gold"]}

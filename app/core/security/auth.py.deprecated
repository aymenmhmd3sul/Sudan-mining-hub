from app.db.compat import users_db
from app.core.security.jwt import decode_token

def get_current_user(token: str):
    payload = decode_token(token)
    if not payload:
        return None

    user_id = payload.get("user_id")
    role = payload.get("role", "user")

    users = users_db()
    user = users.get(user_id)

    if not user:
        return None

    return {
        "id": user_id,
        "role": role
    }

def require_role(user, role: str):
    return user and user.get("role") == role

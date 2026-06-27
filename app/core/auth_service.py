from app.db.database import get_user, get_user_from_cookie


def authenticate_user(email: str, password: str):
    user = get_user(email)

    if not user:
        return None

    if user.get("password") != password:
        return None

    return user


def resolve_user_from_token(token: str):
    if not token:
        return None

    return get_user_from_cookie(token)

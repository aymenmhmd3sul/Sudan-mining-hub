from app.core.security.jwt import create_token
from app.db.compat import users_db


def login_user(email: str, password: str):
    users = users_db()

    for user_id, user in users.items():
        if user["email"] == email and user["password"] == password:

            token = create_token(
                user_id=user_id,
                role=user["role"]
            )

            return {
                "access_token": token,
                "token_type": "bearer"
            }

    return None

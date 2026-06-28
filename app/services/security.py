from fastapi import HTTPException


def assert_user_valid(user):
    if not user or "id" not in user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return True

from fastapi import Request, HTTPException, Depends
from app.core.security.jwt import decode_token

def get_current_user(request: Request):

    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth.replace("Bearer ", "").strip()

    try:
        user = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not user:
        raise HTTPException(status_code=401, detail="Unauthenticated")

    return user


def require_role(*roles):
    def checker(user=Depends(get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return checker

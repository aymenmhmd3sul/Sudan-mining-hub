from fastapi import Depends, HTTPException
from app.core.security.deps import get_current_user

def require_role(*roles):
    def dependency(user=Depends(get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return dependency

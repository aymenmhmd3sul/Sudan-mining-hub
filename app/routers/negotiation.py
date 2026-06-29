from fastapi import APIRouter, Depends, HTTPException
from app.core.security.rbac import require_role

router = APIRouter(prefix="/negotiation", tags=["negotiation"])

@router.post("/rooms")
def create_room(
    offer_id: int,
    user = Depends(require_role("buyer"))
):

    if user["role"] == "seller":
        raise HTTPException(status_code=400, detail="Self negotiation not allowed")

    return {
        "message": "room created",
        "offer_id": offer_id,
        "user": user["sub"]
    }

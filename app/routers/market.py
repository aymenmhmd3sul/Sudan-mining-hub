from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/offers")
def get_offers(user=Depends(get_current_user)):
    return {
        "status": "ok",
        "data": "offers endpoint working",
        "user": user
    }

@router.get("/requests")
def get_requests(user=Depends(get_current_user)):
    return {
        "status": "ok",
        "data": "requests endpoint working",
        "user": user
    }

from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["Chat System"])

@router.get("/{opportunity_id}/{buyer_id}/{seller_id}")
async def get_chat(opportunity_id: int, buyer_id: int, seller_id: int):
    return {"message": "Chat data access"}

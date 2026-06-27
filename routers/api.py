from fastapi import APIRouter
from app.db.compat import get_gold_price

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/gold")
async def gold_price():
    return {"gold": await get_gold_price()}

@router.get("/price")
async def price():
    return {"gold": await get_gold_price()}

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/orders/create")
async def create_order():
    return {"message": "تم إنشاء الطلب بنجاح (تم التوسع هنا لاحقاً)"}

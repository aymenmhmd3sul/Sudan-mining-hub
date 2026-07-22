from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin/offers", tags=["Offers"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def get_offers_page(request: Request):
    sample_offers = [
        {"id": 1, "title": "عرض توريد معدات حفر", "category": "معدات", "price": "15,000 USD", "status": "نشط"},
        {"id": 2, "title": "شراء خام ذهب - كمية 2 كيلو", "category": "خام", "price": "130,000 SDG", "status": "قيد المراجعة"}
    ]
    return templates.TemplateResponse("admin/offers/index.html", {"request": request, "offers": sample_offers})

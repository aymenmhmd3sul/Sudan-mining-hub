from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin/finance", tags=["Admin Escrow"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/escrow", response_class=HTMLResponse)
async def admin_escrow_page(request: Request):
    """عرض لوحة التحكم المخصصة لحسابات الضمان"""
    return templates.TemplateResponse("admin/finance/escrow.html", {"request": request})

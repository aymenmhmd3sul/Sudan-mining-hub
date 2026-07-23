from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/admin/finance/escrow", response_class=HTMLResponse)
async def admin_finance_escrow_page(request: Request):
    return templates.TemplateResponse("admin/finance/escrow.html", {"request": request})
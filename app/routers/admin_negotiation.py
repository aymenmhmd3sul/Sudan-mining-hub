from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["Admin Negotiation"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/negotiation", response_class=HTMLResponse)
@router.get("/negotiation/", response_class=HTMLResponse)
@router.get("/negotiation-dashboard", response_class=HTMLResponse)
async def negotiation_dashboard(request: Request):
    return templates.TemplateResponse(
        "admin/negotiation.html", 
        {"request": request, "active_tab": "negotiation"}
    )

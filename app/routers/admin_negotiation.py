from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/admin", tags=["Admin Negotiation"])
from app.services.templates import templates

@router.get("/negotiation", response_class=HTMLResponse)
@router.get("/negotiation/", response_class=HTMLResponse)
@router.get("/negotiation-dashboard", response_class=HTMLResponse)
async def negotiation_dashboard(request: Request):
    return templates.TemplateResponse(
        "admin/negotiation.html", 
        {"request": request, "active_tab": "negotiation"}
    )

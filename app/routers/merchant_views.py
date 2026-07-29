from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/merchant", tags=["Merchant"])
templates = Jinja2Templates(directory="app/templates")

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
@router.get("/workspace/dashboard", response_class=HTMLResponse)
async def merchant_dashboard(request: Request):
    return templates.TemplateResponse("merchant/dashboard/index.html", {"request": request, "lang": "ar", "active_page": "dashboard"})

@router.get("/deals", response_class=HTMLResponse)
async def merchant_deals(request: Request):
    return templates.TemplateResponse("merchant/deals/index.html", {"request": request, "lang": "ar", "active_page": "deals"})

@router.get("/negotiation", response_class=HTMLResponse)
async def merchant_negotiation(request: Request):
    return templates.TemplateResponse("merchant/negotiation/index.html", {"request": request, "lang": "ar", "active_page": "negotiation"})

@router.get("/negotiation/room/{room_id}", response_class=HTMLResponse)
async def merchant_negotiation_room(request: Request, room_id: int):
    return templates.TemplateResponse("merchant/negotiation/room.html", {"request": request, "lang": "ar", "room_id": room_id, "active_page": "negotiation"})

@router.get("/finance", response_class=HTMLResponse)
async def merchant_finance(request: Request):
    return templates.TemplateResponse("merchant/finance/index.html", {"request": request, "lang": "ar", "active_page": "finance"})

@router.get("/trust", response_class=HTMLResponse)
@router.get("/escrow", response_class=HTMLResponse)
@router.get("/guarantee", response_class=HTMLResponse)
async def merchant_escrow(request: Request):
    return templates.TemplateResponse("merchant/trust/index.html", {"request": request, "lang": "ar", "active_page": "guarantee"})

@router.get("/documents", response_class=HTMLResponse)
async def merchant_documents(request: Request):
    return templates.TemplateResponse("merchant/documents/index.html", {"request": request, "lang": "ar", "active_page": "documents"})

@router.get("/profile", response_class=HTMLResponse)
@router.get("/account", response_class=HTMLResponse)
async def merchant_profile(request: Request):
    return templates.TemplateResponse("merchant/profile/index.html", {"request": request, "lang": "ar", "active_page": "profile"})

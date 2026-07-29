from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/merchant", tags=["Merchant"])

templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def merchant_dashboard(request: Request):
    return templates.TemplateResponse(
        "merchant/dashboard/index.html",
        {
            "request": request,
            "lang": "ar"
        }
    )


@router.get("/profile", response_class=HTMLResponse)
async def merchant_profile(request: Request):
    return templates.TemplateResponse(
        "merchant/profile/index.html",
        {"request": request, "lang": "ar"}
    )


@router.get("/trust", response_class=HTMLResponse)
async def merchant_trust(request: Request):
    return templates.TemplateResponse(
        "merchant/trust/index.html",
        {"request": request, "lang": "ar"}
    )


@router.get("/guarantee", response_class=HTMLResponse)
async def merchant_guarantee(request: Request):
    return templates.TemplateResponse(
        "merchant/guarantee/index.html",
        {"request": request, "lang": "ar"}
    )


@router.get("/deals", response_class=HTMLResponse)
async def merchant_deals(request: Request):
    return templates.TemplateResponse(
        "merchant/deals/index.html",
        {"request": request, "lang": "ar"}
    )


@router.get("/negotiation", response_class=HTMLResponse)
async def merchant_negotiation(request: Request):
    return templates.TemplateResponse(
        "merchant/negotiation/index.html",
        {"request": request, "lang": "ar"}
    )


@router.get("/finance", response_class=HTMLResponse)
async def merchant_finance(request: Request):
    return templates.TemplateResponse(
        "merchant/finance/index.html",
        {"request": request, "lang": "ar"}
    )


@router.get("/documents", response_class=HTMLResponse)
async def merchant_documents(request: Request):
    return templates.TemplateResponse(
        "merchant/documents/index.html",
        {"request": request, "lang": "ar"}
    )

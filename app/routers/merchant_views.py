from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.templates import templates, template_context
from app.core.dependencies import require_merchant
from fastapi import Depends

router = APIRouter(
    prefix="/merchant",
    tags=["Merchant"],
    dependencies=[Depends(require_merchant)]
)


@router.get("", response_class=HTMLResponse)
async def merchant_dashboard(request: Request):
    return templates.TemplateResponse(
        "merchant/dashboard/index.html",
        template_context(request)
    )


@router.get("/profile", response_class=HTMLResponse)
async def merchant_profile(request: Request):
    return templates.TemplateResponse(
        "merchant/profile/index.html",
        template_context(request)
    )


@router.get("/trust", response_class=HTMLResponse)
async def merchant_trust(request: Request):
    return templates.TemplateResponse(
        "merchant/trust/index.html",
        template_context(request)
    )


@router.get("/guarantee", response_class=HTMLResponse)
async def merchant_guarantee(request: Request):
    return templates.TemplateResponse(
        "merchant/guarantee/index.html",
        template_context(request)
    )


@router.get("/deals", response_class=HTMLResponse)
async def merchant_deals(request: Request):
    return templates.TemplateResponse(
        "merchant/deals/index.html",
        template_context(request)
    )


@router.get("/negotiation", response_class=HTMLResponse)
async def merchant_negotiation(request: Request):
    return templates.TemplateResponse(
        "merchant/negotiation/index.html",
        template_context(request)
    )


@router.get("/finance", response_class=HTMLResponse)
async def merchant_finance(request: Request):
    return templates.TemplateResponse(
        "merchant/finance/index.html",
        template_context(request)
    )


@router.get("/documents", response_class=HTMLResponse)
async def merchant_documents(request: Request):
    return templates.TemplateResponse(
        "merchant/documents/index.html",
        template_context(request)
    )

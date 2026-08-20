from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.services.templates import templates, template_context
from app.core.dependencies import require_merchant
from app.database import get_db
from app.models.finance import Invoice, Escrow
from app.models.operations import FinancialTransaction


router = APIRouter(
    prefix="/merchant",
    tags=["Merchant"],
    dependencies=[Depends(require_merchant)],
)


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
@router.get("/workspace/dashboard", response_class=HTMLResponse)
async def merchant_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(require_merchant),
):
    active_deals_count = db.query(Invoice).filter(
        Invoice.seller_id == current_user.id
    ).count()

    escrow_balance = db.query(
        func.sum(Escrow.amount)
    ).join(
        Invoice,
        Escrow.invoice_id == Invoice.id
    ).filter(
        Invoice.seller_id == current_user.id
    ).scalar() or 0

    available_balance = db.query(
        func.sum(FinancialTransaction.amount)
    ).filter(
        FinancialTransaction.user_id == current_user.id,
        FinancialTransaction.status == "APPROVED"
    ).scalar() or 0

    context = template_context(request)
    context["active_page"] = "dashboard"
    context["merchant"] = current_user
    context["active_deals_count"] = active_deals_count
    context["escrow_balance"] = escrow_balance
    context["available_balance"] = available_balance

    return templates.TemplateResponse(
        "merchant/dashboard/index.html",
        context,
    )


@router.get("/deals", response_class=HTMLResponse)
async def merchant_deals(request: Request):
    context = template_context(request)
    context["active_page"] = "deals"

    return templates.TemplateResponse(
        "merchant/deals/index.html",
        context,
    )


@router.get("/negotiation", response_class=HTMLResponse)
async def merchant_negotiation(request: Request):
    context = template_context(request)
    context["active_page"] = "negotiation"

    return templates.TemplateResponse(
        "merchant/negotiation/index.html",
        context,
    )


@router.get("/negotiation/room/{room_id}", response_class=HTMLResponse)
async def merchant_negotiation_room(
    request: Request,
    room_id: int,
):
    context = template_context(request)
    context["room_id"] = room_id
    context["active_page"] = "negotiation"

    return templates.TemplateResponse(
        "merchant/negotiation/room.html",
        context,
    )


@router.get("/finance", response_class=HTMLResponse)
async def merchant_finance(request: Request):
    context = template_context(request)
    context["active_page"] = "finance"

    return templates.TemplateResponse(
        "merchant/finance/index.html",
        context,
    )


@router.get("/trust", response_class=HTMLResponse)
@router.get("/escrow", response_class=HTMLResponse)
async def merchant_trust(request: Request):
    context = template_context(request)
    context["active_page"] = "trust"

    return templates.TemplateResponse(
        "merchant/trust/index.html",
        context,
    )


@router.get("/guarantee", response_class=HTMLResponse)
async def merchant_guarantee(request: Request):
    context = template_context(request)
    context["active_page"] = "guarantee"

    return templates.TemplateResponse(
        "merchant/guarantee/index.html",
        context,
    )


@router.get("/documents", response_class=HTMLResponse)
async def merchant_documents(request: Request):
    context = template_context(request)
    context["active_page"] = "documents"

    return templates.TemplateResponse(
        "merchant/documents/index.html",
        context,
    )


@router.get("/profile", response_class=HTMLResponse)
@router.get("/account", response_class=HTMLResponse)
async def merchant_profile(request: Request):
    context = template_context(request)
    context["active_page"] = "profile"

    return templates.TemplateResponse(
        "merchant/profile/index.html",
        context,
    )

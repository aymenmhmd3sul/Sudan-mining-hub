from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.security.auth import get_current_user
from app.database import get_db
from app.models.finance import Invoice, Escrow
from app.models.user import User
from app.models.marketplace import MiningAsset
from app.models.operations import FinancialTransaction
from app.models.negotiation import MarketDeal, NegotiationMessage
from app.viewmodels.merchant_dashboard import map_invoice

router = APIRouter(prefix="/merchant", tags=["Merchant"])
templates = Jinja2Templates(directory="app/templates")

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
@router.get("/workspace/dashboard", response_class=HTMLResponse)
async def merchant_dashboard(
    request: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
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
        Invoice.seller_id == current_user.id,
        Escrow.status == "HELD"
    ).scalar() or 0

    available_balance = db.query(
        func.sum(FinancialTransaction.amount)
    ).filter(
        FinancialTransaction.user_id == current_user.id,
        FinancialTransaction.status == "APPROVED"
    ).scalar() or 0

    # NOTE:
    # Temporary calculation until commission engine activation.
    # Future version will calculate true merchant net profit
    # after commissions, fees and taxes.

    monthly_profit = db.query(
        func.sum(Invoice.total_amount)
    ).filter(
        Invoice.seller_id == current_user.id,
        Invoice.status.in_(["PAID", "completed"])
    ).scalar() or 0

            
    recent_invoices = db.query(Invoice).filter(
        Invoice.seller_id == current_user.id
    ).order_by(
        Invoice.created_at.desc()
    ).limit(5).all()

    recent_deals = [
        map_invoice(invoice)
        for invoice in recent_invoices
    ]

    return templates.TemplateResponse(
        "merchant/dashboard/index.html",
        {
            "request": request,
            "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr",
            "active_page": "dashboard",
            "merchant": current_user,
            "active_deals_count": active_deals_count,
            "escrow_balance": escrow_balance,
            "available_balance": available_balance,
        "monthly_profit": monthly_profit,
        "recent_deals": recent_deals
        }
    )

@router.get("/deals", response_class=HTMLResponse)
async def merchant_deals(
    request: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    invoices = db.query(Invoice).filter(
        Invoice.seller_id == current_user.id
    ).order_by(
        Invoice.created_at.desc()
    ).all()

    deals = [
        map_invoice(invoice)
        for invoice in invoices
    ]

    return templates.TemplateResponse(
        "merchant/deals/index.html",
        {
            "request": request,
            "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr",
            "active_page": "deals",
            "deals": deals,
            "deals_count": len(deals)
        }
    )

@router.get("/negotiation", response_class=HTMLResponse)
async def merchant_negotiation(
    request: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rooms = db.query(MarketDeal).filter(
        MarketDeal.seller_id == current_user.id
    ).order_by(
        MarketDeal.updated_at.desc()
    ).all()

    negotiation_rooms = []

    for room in rooms:
        last_message = db.query(NegotiationMessage).filter(
            NegotiationMessage.room_id == room.id
        ).order_by(
            NegotiationMessage.created_at.desc()
        ).first()

        negotiation_rooms.append({
            "id": room.id,
            "buyer_name": room.buyer.name if room.buyer else f"المشتري {room.buyer_id}",
            "status": room.status,
            "message": last_message.message if last_message else "لا توجد رسائل",
            "updated_at": room.updated_at
        })

    return templates.TemplateResponse(
        "merchant/negotiation/index.html",
        {
            "request": request,
            "rooms": negotiation_rooms,
            "rooms_count": len(negotiation_rooms),
            "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr",
            "active_page": "negotiation"
        }
    )

@router.get("/negotiation/room/{room_id}", response_class=HTMLResponse)
async def merchant_negotiation_room(request: Request, room_id: int):
    return templates.TemplateResponse("merchant/negotiation/room.html", {"request": request, "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr", "room_id": room_id, "active_page": "negotiation"})

@router.get("/finance", response_class=HTMLResponse)
async def merchant_finance(request: Request):
    return templates.TemplateResponse("merchant/finance/index.html", {"request": request, "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr", "active_page": "finance"})

@router.get("/trust", response_class=HTMLResponse)
@router.get("/escrow", response_class=HTMLResponse)
@router.get("/guarantee", response_class=HTMLResponse)
async def merchant_escrow(request: Request):
    return templates.TemplateResponse("merchant/trust/index.html", {"request": request, "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr", "active_page": "guarantee"})

@router.get("/documents", response_class=HTMLResponse)
async def merchant_documents(request: Request):
    return templates.TemplateResponse("merchant/documents/index.html", {"request": request, "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr", "active_page": "documents"})

@router.get("/profile", response_class=HTMLResponse)
@router.get("/account", response_class=HTMLResponse)
async def merchant_profile(request: Request):
    return templates.TemplateResponse("merchant/profile/index.html", {"request": request, "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr", "active_page": "profile"})


@router.get("/assets", response_class=HTMLResponse)
async def merchant_assets(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    assets = db.query(MiningAsset).filter(
        MiningAsset.owner_id == current_user.id
    ).all()

    return templates.TemplateResponse(
        "merchant/assets/index.html",
        {
            "request": request,
            "assets": assets,
            "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr",
            "active_page": "assets"
        }
    )


@router.get("/assets/new", response_class=HTMLResponse)
async def merchant_new_asset(
    request: Request,
    current_user = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "merchant/assets/new.html",
        {
            "request": request,
            "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr",
            "active_page": "assets",
            "merchant": current_user
        }
    )

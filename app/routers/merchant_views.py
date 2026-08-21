from datetime import datetime
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Form

from app.services.templates import templates, template_context
from app.core.dependencies import require_merchant
from app.database import get_db
from app.models.finance import Invoice, Escrow
from app.models.operations import FinancialTransaction
from app.models.marketplace import MiningAsset, AssetType


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
        Invoice.seller_id == current_user.id,
        Invoice.status.in_(["draft", "pending", "paid"]),
    ).count()

    escrow_balance = db.query(
        func.coalesce(func.sum(Escrow.amount), 0)
    ).join(
        Invoice,
        Escrow.invoice_id == Invoice.id,
    ).filter(
        Invoice.seller_id == current_user.id,
        Escrow.status.in_(["pending", "funded", "disputed"]),
    ).scalar() or 0

    available_balance = db.query(
        func.coalesce(func.sum(FinancialTransaction.amount), 0)
    ).filter(
        FinancialTransaction.user_id == current_user.id,
        FinancialTransaction.status == "APPROVED",
    ).scalar() or 0

    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)
    previous_month_start = (
        datetime(now.year - 1, 12, 1)
        if now.month == 1
        else datetime(now.year, now.month - 1, 1)
    )

    current_month_sales = db.query(
        func.coalesce(func.sum(Invoice.total_amount), 0)
    ).filter(
        Invoice.seller_id == current_user.id,
        Invoice.status.in_(["paid", "completed"]),
        Invoice.created_at >= month_start,
    ).scalar() or 0

    previous_month_sales = db.query(
        func.coalesce(func.sum(Invoice.total_amount), 0)
    ).filter(
        Invoice.seller_id == current_user.id,
        Invoice.status.in_(["paid", "completed"]),
        Invoice.created_at >= previous_month_start,
        Invoice.created_at < month_start,
    ).scalar() or 0

    if previous_month_sales:
        monthly_profit = round(
            ((float(current_month_sales) - float(previous_month_sales))
             / float(previous_month_sales)) * 100,
            1,
        )
    elif current_month_sales:
        monthly_profit = 100.0
    else:
        monthly_profit = 0.0

    latest_deals = db.query(Invoice).filter(
        Invoice.seller_id == current_user.id,
    ).order_by(Invoice.created_at.desc()).limit(5).all()

    context = template_context(request)
    context["active_page"] = "dashboard"
    context["merchant"] = current_user
    context["active_deals_count"] = active_deals_count
    context["escrow_balance"] = escrow_balance
    context["available_balance"] = available_balance
    context["monthly_profit"] = monthly_profit
    context["latest_deals"] = latest_deals

    return templates.TemplateResponse(
        "merchant/dashboard/index.html",
        context,
    )




@router.get("/deals/new", response_class=HTMLResponse)
async def merchant_new_offer(
    request: Request,
    current_user = Depends(require_merchant),
):
    context = template_context(request)
    context["active_page"] = "deals"
    context["form_error"] = None
    return templates.TemplateResponse(
        "merchant/deals/new.html",
        context,
    )


@router.post("/deals/new", response_class=HTMLResponse)
async def merchant_create_offer(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    asset_type: str = Form("product"),
    main_category: str = Form("GENERAL"),
    sub_category: str = Form("GENERAL"),
    price: float = Form(...),
    currency: str = Form("SDG"),
    is_negotiable: bool = Form(False),
    state_province: str = Form(...),
    locality: str = Form(...),
    coordinates: str = Form(""),
    images_urls: str = Form(""),
    specific_specs: str = Form(""),
    other_description: str = Form(""),
    db: Session = Depends(get_db),
    current_user = Depends(require_merchant),
):
    import json

    context = template_context(request)
    context["active_page"] = "deals"
    context["form_error"] = None

    try:
        normalized_type = asset_type.strip().lower()

        allowed_types = {item.value for item in AssetType}
        if normalized_type not in allowed_types:
            raise ValueError("نوع العرض غير صالح.")

        if price <= 0:
            raise ValueError("يجب أن يكون السعر أكبر من صفر.")

        if not title.strip():
            raise ValueError("اسم العرض مطلوب.")

        image_list = [
            item.strip()
            for item in images_urls.split(",")
            if item.strip()
        ]

        specs = {}
        if specific_specs.strip():
            specs = json.loads(specific_specs)

        if not isinstance(specs, dict):
            raise ValueError("المواصفات يجب أن تكون بصيغة JSON صحيحة.")

        new_asset = MiningAsset(
            owner_id=current_user.id,
            title=title.strip(),
            description=description.strip() or None,
            asset_type=AssetType(normalized_type),
            other_description=other_description.strip() or None,
            main_category=main_category.strip() or "GENERAL",
            sub_category=sub_category.strip() or "GENERAL",
            price=price,
            currency=currency.strip().upper() or "SDG",
            is_negotiable=is_negotiable,
            state_province=state_province.strip(),
            locality=locality.strip(),
            coordinates=coordinates.strip() or None,
            images_urls=image_list,
            specific_specs=specs,
            is_featured=False,
            is_approved=False,
            status="ACTIVE",
        )

        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)

        return RedirectResponse(
            url="/merchant/deals?created=1",
            status_code=303,
        )

    except Exception as exc:
        db.rollback()
        context["form_error"] = str(exc)
        return templates.TemplateResponse(
            "merchant/deals/new.html",
            context,
            status_code=400,
        )


@router.get("/deals", response_class=HTMLResponse)
async def merchant_deals(
    request: Request,
    current_user = Depends(require_merchant),
):
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

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
# استخدام نظام التحقق والأمان المطور المعتمد في المنصة
from app.security.auth import get_current_user as require_any_user 
from app.models.marketplace import MiningAsset  # تعديل معماري صارم وصحيح
from app.schemas.assets import AssetCreate, AssetResponse
from app.services.plan_access_service import PlanAccessService

router = APIRouter(prefix="/marketplace", tags=["Asset Marketplace Core"])

@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_mining_asset(
    payload: AssetCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(require_any_user)
):
    """
    نشر أصل تعديني جديد في قاعدة البيانات الموحدة باستخدام SQLAlchemy ORM.
    يدعم تسجيل البيانات وإسنادها للمستخدم الحالي مع تفعيل خاصية الـ Concurrency Control (Version: 1).
    """
    # التحقق من صلاحية المستخدم (البائع أو الأدمن فقط حسب هيكل الصلاحيات)
    user_role = current_user.role.lower()
    if user_role not in ["seller", "merchant", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="عذراً، هذا الإجراء متاح فقط للحسابات المعتمدة كبائع أو تاجر في المنصة."
        )

    
    if user_role != "admin":
        allowed, result = PlanAccessService.can_create_listing(
            db,
            current_user.id
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=result
            )

    try:
        # تحويل القوائم والقواميس إلى JSON Strings لتخزينها في قاعدة البيانات الموحدة
        images_str = json.dumps(payload.images_urls) if payload.images_urls else "[]"
        specs_str = json.dumps(payload.specific_specs) if payload.specific_specs else "{}"

        # بناء الكائن باستخدام SQLAlchemy Model
        new_asset = MiningAsset(
            title=payload.title,
            description=payload.description,
            main_category=payload.main_category,
            sub_category=payload.sub_category,
            price=payload.price,
            currency=payload.currency,
            is_negotiable=payload.is_negotiable,
            owner_id=current_user.id,  # ربط الأصل بالمالك الحالي تلقائياً
            state_province=payload.state_province,
            locality=payload.locality,
            coordinates=payload.coordinates,
            images_urls=images_str,
            specific_specs=specs_str,
            version=1  # تعيين قيمة أولية لإصدار التحكم التزامني (Optimistic Concurrency Version)
        )

        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)
        
        return {
            "id": new_asset.id,
            "owner_id": new_asset.owner_id,
            "title": new_asset.title,
            "description": new_asset.description,
            "main_category": new_asset.main_category,
            "sub_category": new_asset.sub_category,
            "price": new_asset.price,
            "currency": new_asset.currency,
            "is_negotiable": new_asset.is_negotiable,
            "state_province": new_asset.state_province,
            "locality": new_asset.locality,
            "coordinates": new_asset.coordinates,
            "images_urls": json.loads(new_asset.images_urls) if isinstance(new_asset.images_urls, str) else new_asset.images_urls,
            "specific_specs": json.loads(new_asset.specific_specs) if isinstance(new_asset.specific_specs, str) else new_asset.specific_specs,
            "status": new_asset.status,
            "created_at": new_asset.created_at,
            "updated_at": new_asset.updated_at
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء حفظ الأصل التعديني: {str(e)}"
        )


@router.get("/assets", response_model=list[AssetResponse])
def list_mining_assets(
    db: Session = Depends(get_db)
):
    """
    عرض الأصول التعدينية المتاحة في السوق.
    """
    assets = db.query(MiningAsset).filter(
        MiningAsset.status == "ACTIVE"
    ).all()

    return [
        {
            "id": asset.id,
            "owner_id": asset.owner_id,
            "title": asset.title,
            "description": asset.description,
            "main_category": asset.main_category,
            "sub_category": asset.sub_category,
            "price": asset.price,
            "currency": asset.currency,
            "is_negotiable": asset.is_negotiable,
            "state_province": asset.state_province,
            "locality": asset.locality,
            "coordinates": asset.coordinates,
            "images_urls": json.loads(asset.images_urls) if isinstance(asset.images_urls, str) else asset.images_urls,
            "specific_specs": json.loads(asset.specific_specs) if isinstance(asset.specific_specs, str) else asset.specific_specs,
            "status": asset.status,
            "created_at": asset.created_at,
            "updated_at": asset.updated_at
        }
        for asset in assets
    ]


@router.get("/assets/{asset_id}", response_model=AssetResponse)
def get_mining_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    """
    عرض تفاصيل أصل تعديني محدد.
    """
    asset = db.query(MiningAsset).filter(
        MiningAsset.id == asset_id
    ).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الأصل التعديني غير موجود"
        )

    return {
        "id": asset.id,
        "owner_id": asset.owner_id,
        "title": asset.title,
        "description": asset.description,
        "main_category": asset.main_category,
        "sub_category": asset.sub_category,
        "price": asset.price,
        "currency": asset.currency,
        "is_negotiable": asset.is_negotiable,
        "state_province": asset.state_province,
        "locality": asset.locality,
        "coordinates": asset.coordinates,
        "images_urls": json.loads(asset.images_urls) if isinstance(asset.images_urls, str) else asset.images_urls,
        "specific_specs": json.loads(asset.specific_specs) if isinstance(asset.specific_specs, str) else asset.specific_specs,
        "status": asset.status,
        "created_at": asset.created_at,
        "updated_at": asset.updated_at
    }


@router.delete("/assets/{asset_id}")
def delete_mining_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_any_user)
):
    """
    حذف منطقي للأصل التعديني.
    لا يتم حذف السجل من قاعدة البيانات.
    """

    asset = db.query(MiningAsset).filter(
        MiningAsset.id == asset_id
    ).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الأصل التعديني غير موجود"
        )

    user_role = current_user.role.lower()

    if asset.owner_id != current_user.id and user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية حذف هذا الأصل"
        )

    asset.status = "DELETED"

    db.commit()
    db.refresh(asset)

    return {
        "message": "تم حذف الأصل بشكل منطقي",
        "asset_id": asset.id,
        "status": asset.status
    }


@router.patch("/assets/{asset_id}", response_model=AssetResponse)
def update_mining_asset(
    asset_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user = Depends(require_any_user)
):
    """
    تحديث بيانات الأصل التعديني.
    يدعم التحديث الجزئي مع رفع إصدار الحماية.
    """

    asset = db.query(MiningAsset).filter(
        MiningAsset.id == asset_id
    ).first()

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="الأصل التعديني غير موجود"
        )

    user_role = current_user.role.lower()

    if asset.owner_id != current_user.id and user_role != "admin":
        raise HTTPException(
            status_code=403,
            detail="ليس لديك صلاحية تعديل هذا الأصل"
        )

    allowed_fields = [
        "title",
        "description",
        "main_category",
        "sub_category",
        "price",
        "currency",
        "is_negotiable",
        "state_province",
        "locality",
        "coordinates",
        "images_urls",
        "specific_specs"
    ]

    for field in allowed_fields:
        if field in payload:
            value = payload[field]

            if field == "images_urls":
                value = json.dumps(value)

            if field == "specific_specs":
                value = json.dumps(value)

            setattr(asset, field, value)

    asset.version = (asset.version or 1) + 1

    db.commit()
    db.refresh(asset)

    return {
        "id": asset.id,
        "owner_id": asset.owner_id,
        "title": asset.title,
        "description": asset.description,
        "main_category": asset.main_category,
        "sub_category": asset.sub_category,
        "price": asset.price,
        "currency": asset.currency,
        "is_negotiable": asset.is_negotiable,
        "state_province": asset.state_province,
        "locality": asset.locality,
        "coordinates": asset.coordinates,
        "images_urls": json.loads(asset.images_urls) if isinstance(asset.images_urls, str) else asset.images_urls,
        "specific_specs": json.loads(asset.specific_specs) if isinstance(asset.specific_specs, str) else asset.specific_specs,
        "status": asset.status,
        "created_at": asset.created_at,
        "updated_at": asset.updated_at
    }

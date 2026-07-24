import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
# استخدام نظام التحقق والأمان المطور المعتمد في المنصة
from app.security.auth import get_current_user as require_any_user 
from app.models.marketplace import MiningAsset  # تعديل معماري صارم وصحيح
from app.schemas.assets import AssetCreate, AssetResponse

router = APIRouter(prefix="/marketplace", tags=["Asset Marketplace Core"])

@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_mining_asset(
    payload: AssetCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(require_any_user)
):
    """
    نشر أصل تعديني جديد في قاعدة البيانات الموحدة باستخدام SQLAlchemy ORM.
    يدعم تسجيل البيانات وإسنادها للمستخدم الحالي مع تفعيل خاصية الـ Concurrency Control (Version: 1).
    """
    # التحقق من صلاحية المستخدم (البائع أو الأدمن فقط حسب هيكل الصلاحيات)
    user_role = current_user.get("role")
    if user_role not in ["seller", "merchant", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="عذراً، هذا الإجراء متاح فقط للحسابات المعتمدة كبائع أو تاجر في المنصة."
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
            owner_id=current_user["id"],  # ربط الأصل بالمالك الحالي تلقائياً
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
        
        return new_asset

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء حفظ الأصل التعديني: {str(e)}"
        )

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import json
from typing import List, Optional
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.marketplace import MiningAsset
from app.schemas.assets import AssetCreate, AssetResponse

router = APIRouter(prefix="/market", tags=["Market Core"])

# مساعد لفك نصوص JSON القادمة من SQLite إلى كائنات بايثون لتتوافق مع الـ Schema
def format_asset_response(asset: MiningAsset) -> dict:
    if not asset:
        return None
    from datetime import datetime
    res = {c.name: getattr(asset, c.name) for c in asset.__table__.columns}
    if isinstance(res.get("images_urls"), str):
        try: res["images_urls"] = json.loads(res["images_urls"])
        except: res["images_urls"] = []
    if isinstance(res.get("specific_specs"), str):
        try: res["specific_specs"] = json.loads(res["specific_specs"])
        except: res["specific_specs"] = {}
    if res.get("created_at") is None:
        res["created_at"] = datetime.utcnow()
    return res

# 1. إنشاء أصل جديد (تم تثبيته مسبقاً)
@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_data: AssetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    data_dict = asset_data.dict() if hasattr(asset_data, "dict") else asset_data.model_dump()
    is_sqlite = db.bind.dialect.name == "sqlite"
    if is_sqlite:
        if "images_urls" in data_dict and isinstance(data_dict["images_urls"], list):
            data_dict["images_urls"] = json.dumps(data_dict["images_urls"])
        if "specific_specs" in data_dict and isinstance(data_dict["specific_specs"], dict):
            data_dict["specific_specs"] = json.dumps(data_dict["specific_specs"])
            
    for key, value in data_dict.items():
        setattr(asset, key, value)
        
    db.commit()
    db.refresh(asset)
    return format_asset_response(asset)

# 5. الحذف المنطقي (Soft Delete) لحماية البيانات وتاريخ المنصة
@router.delete("/assets/{asset_id}", status_code=status.HTTP_200_OK)
async def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    asset = db.query(MiningAsset).filter(MiningAsset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="الأصل غير موجود")
    if asset.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="غير مصرح لك بحذف هذا الأصل")
        
    # اعتماد الحذف المنطقي بجعل الحالة DELETED بدلاً من الحذف الفيزيائي المفاجئ
    asset.status = "DELETED"
    db.commit()
    return {"detail": "تم حذف الأصل بنجاح (حذف منطقي)"}

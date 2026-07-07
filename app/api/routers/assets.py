from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.marketplace import MiningAsset
from app.schemas.assets import AssetCreate, AssetResponse

router = APIRouter(prefix="/market", tags=["Market Core"])

@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_data: AssetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # حل جذري للتوافق مع إصدارات Pydantic المختلفة
    data_dict = asset_data.dict() if hasattr(asset_data, "dict") else asset_data.model_dump()
    
    # معالجة ذكية لتحويل المصفوفات والقواميس إلى نصوص متوافقة مع SQLite
    for key, value in data_dict.items():
        if isinstance(value, (list, dict)):
            data_dict[key] = json.dumps(value)

    new_asset = MiningAsset(
        owner_id=current_user.id,
        **data_dict
    )
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset

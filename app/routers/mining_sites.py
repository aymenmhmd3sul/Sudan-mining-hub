from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.security.auth import get_current_user as require_any_user
from app.models.mining_site import MiningSite
from app.schemas.mining_site import MiningSiteCreate, MiningSiteResponse

router = APIRouter(prefix="/mining-sites", tags=["Mining Sites Management"])

@router.post("/", response_model=MiningSiteResponse, status_code=status.HTTP_201_CREATED)
def create_mining_site(
    payload: MiningSiteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_any_user)
):
    user_role = current_user.get("role")
    if user_role not in ["investor", "engineer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="عذراً، هذا الإجراء متاح فقط للحسابات المعتمدة كأدمن، مهندس، أو مستثمر."
        )
    try:
        new_site = MiningSite(
            name=payload.name,
            description=payload.description,
            resource_type=payload.resource_type,
            state_province=payload.state_province,
            locality=payload.locality,
            coordinates=payload.coordinates,
            owner_id=current_user["id"],
            version=1
        )
        db.add(new_site)
        db.commit()
        db.refresh(new_site)
        return new_site
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء حفظ موقع التعدين: {str(e)}"
        )

@router.get("/", response_model=List[MiningSiteResponse])
def list_mining_sites(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_any_user)
):
    return db.query(MiningSite).all()

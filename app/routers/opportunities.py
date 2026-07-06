from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.security.auth import get_db, get_current_user
from app.models.identity import User
from app.models.opportunities import Opportunity
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/opportunity-center", tags=["Opportunity Center (Investments & Tenders)"])

class OpportunityCreate(BaseModel):
    title: str
    opportunity_type: str    # INVESTMENT, TENDER, AUCTION, FUNDING
    description: str
    target_amount: float = None

@router.post("/create")
def create_opportunity(req: OpportunityCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """نشر فرصة استثمارية، عطاء، أو طلب تمويل جديد في المركز"""
    opp = Opportunity(
        creator_id=current_user.id,
        title=req.title,
        opportunity_type=req.opportunity_type.upper(),
        description=req.description,
        target_amount=req.target_amount
    )
    db.add(opp)
    db.commit()
    return {"message": "✅ تم نشر الفرصة الاستثمارية بنجاح في مركز الفرص العام!"}

@router.get("/explore")
def explore_opportunities(opp_type: str = None, db: Session = Depends(get_db)):
    """استكشاف الفرص الاستثمارية والعطاءات المتاحة للمستثمرين والتجار"""
    query = db.query(Opportunity).filter(Opportunity.status == "OPEN")
    if opp_type:
        query = query.filter(Opportunity.opportunity_type == opp_type.upper())
    return {"status": "success", "data": query.all()}

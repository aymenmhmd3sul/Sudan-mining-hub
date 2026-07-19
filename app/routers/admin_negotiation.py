from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.admin_negotiation_service import AdminNegotiationService

router = APIRouter(
    prefix="/admin/operations",
    tags=["Admin Negotiation"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/negotiation-dashboard")
def negotiation_dashboard(db: Session = Depends(get_db)):
    return AdminNegotiationService.get_dashboard(db)

from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class DisputeStatus(str, Enum):
    OPEN = "open"
    UNDER_REVIEW = "under_review"
    WAITING_FOR_PARTIES = "waiting_for_parties"
    RESOLVED = "resolved"
    REJECTED = "rejected"
    CLOSED = "closed"

class DisputeBase(BaseModel):
    invoice_id: int
    escrow_id: int
    payment_id: int
    opened_by: int
    reason: str
    description: str
    status: DisputeStatus = DisputeStatus.OPEN

class DisputeCreate(DisputeBase):
    pass

class Dispute(DisputeBase):
    id: int
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

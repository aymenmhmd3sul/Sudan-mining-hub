from pydantic import BaseModel
from typing import Optional, List

# --- نماذج المحادثات القديمة المستقرة ---
class CreateRoomPayload(BaseModel):
    asset_id: int

class SendMessagePayload(BaseModel):
    message: str
    offer_price: Optional[float] = None

class RoomStatusPayload(BaseModel):
    status: str

# --- نماذج محرك العقود والـ Milestones الموحد الجديد ---
class DealCreatePayload(BaseModel):
    listing_id: int
    buyer_id: int
    final_price: float
    currency: str = "SDG"
    milestones: List[str] # قائمة بعناوين الخطوات (فحص، شحن، توريد)

class MilestoneUpdatePayload(BaseModel):
    status: str # PENDING, IN_PROGRESS, VERIFIED, FAILED

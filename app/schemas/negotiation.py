from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

# --- 1. تعريف الـ Enums لضمان الـ Validation وحماية الـ Swagger ---
class RoomStatus(str, Enum):
    OPEN = "OPEN"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"

class MessageType(str, Enum):
    TEXT = "TEXT"
    OFFER = "OFFER"
    SYSTEM = "SYSTEM"

class OfferStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

# --- 2. Schemas العروض المادية (Offers) ---
class OfferCreate(BaseModel):
    amount: float = Field(..., gt=0, description="قيمة العرض المالي المطلوب")
    currency: Optional[str] = Field("USD", description="العملة المستخدمة")

class OfferResponse(BaseModel):
    id: int
    room_id: int
    amount: float
    currency: str
    status: OfferStatus
    created_at: datetime

    class Config:
        from_attributes = True

# --- 3. Schemas الرسائل (Messages) ---
class MessageCreate(BaseModel):
    message: str = Field(..., min_length=1, description="نص الرسالة أو تفاصيل العرض")
    message_type: Optional[MessageType] = Field(MessageType.TEXT, description="نوع الرسالة")

class MessageResponse(BaseModel):
    id: int
    room_id: int
    sender_id: int
    message: str
    message_type: MessageType
    created_at: datetime

    class Config:
        from_attributes = True

# --- 4. Schemas غرف التفاوض (Rooms) ---
class RoomCreate(BaseModel):
    asset_id: int = Field(..., description="معرف المعدة أو الأصل المراد التفاوض عليه")

class RoomResponse(BaseModel):
    id: int
    asset_id: int
    seller_id: int
    buyer_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # حقول التوسع المستقبلية دون كسر الـ API الحالي
    last_message_at: Optional[datetime] = Field(None, description="وقت آخر رسالة مرسلة")
 
    class Config:
        from_attributes = True
    unread_count: Optional[int] = Field(0, description="عدد الرسائل غير المقروءة للمستخدم الحالي")
    last_offer_id: Optional[int] = Field(None, description="معرف آخر عرض مالي نشط في الغرفة")

    class Config:
        from_attributes = True

# مخطط تفصيلي متكامل للغرفة (تفاصيل المحادثة)
class RoomDetailResponse(RoomResponse):
    messages: List[MessageResponse] = Field(default_factory=list, description="سجل الرسائل داخل الغرفة")
    offers: List[OfferResponse] = Field(default_factory=list, description="سجل العروض المالية الرسمية")

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MiningSiteBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, description="اسم موقع التعدين")
    description: Optional[str] = None
    resource_type: str = Field(..., description="نوع الخام")
    state_province: str = Field(..., description="الولاية")
    locality: str = Field(..., description="المحلية")
    coordinates: Optional[str] = Field(None, description="الإحداثيات")

class MiningSiteCreate(MiningSiteBase):
    pass

class MiningSiteResponse(MiningSiteBase):
    id: int
    owner_id: int
    status: str
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

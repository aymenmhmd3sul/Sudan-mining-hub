from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 1. شيمات المستخدمين
class UserBase(BaseModel):
    full_name: str = Field(..., max_length=150)
    email: EmailStr = Field(...)
    role: str = Field("IMPORTER")
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# 2. شيمات الفواتير الدولية (البديل الفعلي للفرص)
class InvoiceBase(BaseModel):
    invoice_title: str = Field(..., max_length=200)
    business_sector: str = Field("MINING")
    amount: float = Field(..., gt=0)
    currency: str = Field("USD")
    target_country: str = Field(...)
    invoice_file_url: Optional[str] = None
    market_status: str = Field("OPEN")

class InvoiceResponse(InvoiceBase):
    id: int
    client_id: int
    created_at: datetime
    class Config:
        orm_mode = True

# 3. شيمات لوحة التحكم الفعلية الموائمة للـ الـ Routers
class DashboardMetricsResponse(BaseModel):
    status: str = "success"
    active_invoices_count: int = Field(..., gte=0)
    total_settlement_amount_usd: float = Field(..., gte=0)
    active_bids_count: int = Field(..., gte=0)
    completed_settlements: int = Field(..., gte=0)

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

# إعادة تعريف الـ Enums على مستوى الـ Schema للتطابق
class OrganizationRole(str, Enum):
    OWNER = "OWNER"
    EXECUTIVE_MANAGER = "EXECUTIVE_MANAGER"
    SALES_MANAGER = "SALES_MANAGER"
    FINANCE_MANAGER = "FINANCE_MANAGER"
    LABORATORY_MANAGER = "LABORATORY_MANAGER"
    LOGISTICS_MANAGER = "LOGISTICS_MANAGER"

class OrganizationStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"

# --- Schemas الخاصة بالمؤسسة (Organization) ---
class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="اسم الشركة أو المؤسسة")
    registration_number: Optional[str] = Field(None, description="السجل التجاري أو الرقم الضريبي")
    business_type: str = Field(..., description="نوع العمل التجاري مثل MINING_COMPANY")

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int
    status: OrganizationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Schemas الخاصة بالعضوية (Membership) ---
class MembershipBase(BaseModel):
    user_id: int
    role: OrganizationRole
    is_active: bool = True

class MembershipCreate(BaseModel):
    user_email: str = Field(..., description="بريد المستخدم المراد دعوته للمؤسسة")
    role: OrganizationRole

class MembershipResponse(MembershipBase):
    id: int
    organization_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- الاستجابة الكاملة للمؤسسة مع أعضائها ---
class OrganizationDetailResponse(OrganizationResponse):
    memberships: List[MembershipResponse] = []

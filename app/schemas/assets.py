from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AssetCreate(BaseModel):
    title: str = Field(..., example="حفار كاتر بيلر 320D")
    description: Optional[str] = None
    main_category: str = Field(..., example="MINING_EQUIPMENT")
    sub_category: str = Field(..., example="EXCAVATOR")
    price: float
    currency: str = "USD"
    is_negotiable: bool = True
    state_province: str = Field(..., example="ولاية نهر النيل")
    locality: str = Field(..., example="أبوحمد")
    coordinates: Optional[str] = None
    images_urls: List[str] = []
    # 🧠 هنا قلب المرونة المعمارية: استقبال أي مواصفات خاصة كقاموس بايثون تلقائي
    specific_specs: Dict[str, Any] = Field(default_factory=dict, example={
        "brand": "CAT", "model": "320D", "working_hours": 6400, "condition": "Excellent"
    })

class AssetResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    main_category: str
    sub_category: str
    price: float
    currency: str
    is_negotiable: bool
    state: str
    owner_id: str
    state_province: str
    locality: str
    coordinates: Optional[str]
    images_urls: List[str]
    specific_specs: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

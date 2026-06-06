from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

# 1. جدول مواقع التعدين (توسيع الحقول حسب مقترحك)
class MiningSite(SQLModel, table=True):
    __tablename__ = "mining_sites"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    state: str  # الولاية
    coordinates: Optional[str] = None  # الإحداثيات (GPS)
    is_active: bool = Field(default=True)

# 2. جدول المعدات والآليات
class Equipment(SQLModel, table=True):
    __tablename__ = "equipment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # اسم المعدة / الآلية
    owner: str  # المالك
    status: str = Field(default="active")  # الحالة التشغيلية
    last_maintenance: Optional[str] = None  # تاريخ الصيانة

# 3. جدول الإنتاجية اليومية
class Production(SQLModel, table=True):
    __tablename__ = "production"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    site_id: int  # ربط بالموقع
    ore_weight: float  # كمية الخام (بالطن مثلاً)
    gold_weight: float  # كمية الذهب المستخلص (بالجرام)
    date: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

# 4. جدول أسعار الذهب والعملات
class GoldPrice(SQLModel, table=True):
    __tablename__ = "gold_prices"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    local_price: float  # السعر المحلي للجرام
    global_ounce: float  # سعر الأونصة العالمي
    usd_rate: float  # سعر الدولار مقابل الجنيه
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

# 5. جدول البلاغات والطوارئ للميدان
class Report(SQLModel, table=True):
    __tablename__ = "reports"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    site_id: int
    report_type: str  # (أعطال، سرقات، مخالفات، طلب صيانة)
    details: str  # تفاصيل البلاغ
    status: str = Field(default="pending")  # (قيد المراجعة، تم الحل)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

# =======================================================
# التحديث الجديد: نظام المخزن الافتراضي والعمولات المرنة للمعدات
# =======================================================

# 6. جدول طلبات الشراء (المشتري يطلب أولاً والرقم مخفي)
class EquipmentOrder(SQLModel, table=True):
    __tablename__ = "equipment_orders"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    buyer_name: str         # اسم المشتري أو الشركة طالبة المعدة
    buyer_phone: str        # رقم الهاتف (مخفي، يظهر فقط بعد قبول العرض النهائي)
    equipment_type: str     # نوع المعدة المطلوبة (بوكلين، جرار، طاحونة، إلخ)
    specifications: str     # المواصفات الفنية والشروط المطلوبة بدقة
    status: str = Field(default="نشط") # حالة الطلب: نشط / تم الاتفاق
    created_at: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

# 7. جدول عروض الأسعار السرية من التجار (المخزن الافتراضي)
class MerchantBid(SQLModel, table=True):
    __tablename__ = "merchant_bids"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int           # ربط العرض برقم طلب المشتري (EquipmentOrder)
    merchant_name: str      # اسم التاجر من الـ 7 تجار لتعريف العرض داخلياً
    merchant_phone: str     # رقم هاتف التاجر (مخفي تماماً عن المشتري حتى الاتفاق المعاين)
    price: float            # السعر المعروض للمعدة
    currency: str           # العملة المحددة (جنيه سوداني / درهم إماراتي / دولار)
    location_in_sudan: str  # موقع المعدة الجغرافي الفعلي (أبو حمد، بربر، العبيدية، إلخ)
    image_url: Optional[str] = Field(default=None) # رابط صورة المعدة ليعاينها المشتري بصرياً قبل الشراء
    
    # تفاصيل العمولة (يدفعها التاجر وهي قابلة للتفاوض)
    commission_rate: float = Field(default=1.0) # نسبة العمولة الافتراضية المقترحة (مثال: 1.0 تعني 1%)
    commission_text: str = Field(default="العمولة قابلة للتفاوض بين 0.5% إلى 2% أو أكثر")
    
    created_at: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

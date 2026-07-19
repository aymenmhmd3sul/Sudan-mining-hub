from sqlalchemy.orm import Session
from app.models.market import PriceAudit
from app.services.oracle_service import OracleService

class MarketService:
    def __init__(self, db: Session):
        self.db = db
        self.oracle = OracleService()

    def get_current_local_price(self):
        """جلب آخر سعر محلي مسجل في النظام"""
        latest = self.db.query(PriceAudit).order_by(PriceAudit.timestamp.desc()).first()
        if latest:
            return latest.new_price
        return 72500.0 # سعر افتراضي في حال كانت قاعدة البيانات فارغة

    def get_market_stats(self):
        """تجميع بيانات السوق وتجهيزها للواجهة"""
        global_data = self.oracle.get_global_gold_price()
        local_price = self.get_current_local_price()
        
        # تجهيز الهيكل المتفق عليه في Schema
        return {
            "gold_spot": global_data,
            "gold_local": {
                "price": local_price,
                "currency": "SDG",
                "unit": "gram",
                "trend": "+0.8%",
                "manual_override": True
            },
            "premium_percent": 7.1, # سيتم برمجتها لاحقاً لعملية حسابية دقيقة
            "market_activity": {
                "volume_24h": 15400000,
                "active_deals": 5,
                "active_merchants": 32
            },
            "oracle": self.oracle.get_status()
        }

    def update_local_price(self, new_price: float, reason: str, admin_id: int):
        """تحديث السعر المحلي وتسجيل العملية في سجل التدقيق"""
        old_price = self.get_current_local_price()
        
        audit_entry = PriceAudit(
            old_price=old_price,
            new_price=new_price,
            reason=reason,
            admin_id=admin_id
        )
        self.db.add(audit_entry)
        self.db.commit()
        self.db.refresh(audit_entry)
        return audit_entry

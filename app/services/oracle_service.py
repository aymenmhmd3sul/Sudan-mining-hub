from datetime import datetime

class OracleService:
    def get_global_gold_price(self):
        """جلب السعر العالمي للذهب (Mock Data للاختبار)"""
        return {
            "price": 3420.5,
            "currency": "USD",
            "unit": "oz",
            "trend": "+1.2%"
        }
    
    def get_status(self):
        """حالة مزود البيانات"""
        return {
            "status": "healthy",
            "sources": ["mock_provider_a", "mock_provider_b"],
            "last_sync": datetime.utcnow()
        }

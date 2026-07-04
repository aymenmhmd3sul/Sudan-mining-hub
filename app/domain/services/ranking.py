from datetime import datetime
from typing import Dict, Any, List

class MarketRankingEngine:
    """ محرك الترتيب والتنظيم الذكي لأسواق قطاع التعدين لعام 2026 """
    
    @staticmethod
    def calculate_asset_score(asset: Any, view_mode: str = "MARKET_FLOW") -> float:
        """
        حساب نقاط الظهور الديناميكية للأصل بناءً على الرؤية الفلسفية للسوق السوداني
        """
        # 1. تحديد أوزان الترتيب حسب وضع العرض المختار
        if view_mode == "TRUSTED_FIRST":
            w_fresh, w_trust, w_activity = 0.2, 0.6, 0.2
        elif view_mode == "INVESTOR_VIEW":
            w_fresh, w_trust, w_activity = 0.1, 0.5, 0.4
        else:  # MARKET_FLOW (الوضع الافتراضي التصفحي)
            w_fresh, w_trust, w_activity = 0.7, 0.1, 0.2

        # 2. حساب عامل الحداثة (Freshness Score)
        # نقيس عمر الإعلان بالأيام؛ إذا كان جديداً يحصل على الدرجة الكاملة
        days_old = (datetime.utcnow() - asset.created_at).days
        s_fresh = max(0.0, 100.0 - (days_old * 2.0))  # يفقد نقطتين كل يوم

        # 3. جلب مؤشر الثقة (Trust Score)
        s_trust = float(getattr(asset, 'trust_score', 50.0))

        # 4. حساب مؤشر نشاط السوق والتفاعلات (Activity Score)
        views = int(getattr(asset, 'views_count', 0))
        favs = int(getattr(asset, 'favorites_count', 0))
        s_activity = min(100.0, (views * 1.0) + (favs * 5.0)) # سقف النشاط 100 لحماية العدالة

        # 5. احتساب مكافآت الشارات البصرية (Tier Bonus)
        s_bonus = 0.0
        tier = getattr(asset, 'listing_tier', 'OPEN')
        if tier == "PREMIUM":
            s_bonus = 30.0
        elif tier == "VERIFIED":
            s_bonus = 15.0

        # 6. المعادلة المركبة النهائية
        total_score = (w_fresh * s_fresh) + (w_trust * s_trust) + (w_activity * s_activity) + s_bonus
        return round(total_score, 2)

    @staticmethod
    def attach_human_badges(asset: Any, score: float) -> Dict[str, Any]:
        """
        تحويل الجفاف التقني إلى لمسات بشرية تناسب ثقافة المجتمع التعديني
        """
        tier = getattr(asset, 'listing_tier', 'OPEN')
        views = int(getattr(asset, 'views_count', 0))
        
        # مصفوفة الألقاب المجتمعية الذكية
        market_label = "🔎 جديد في السوق"
        if tier == "PREMIUM":
            market_label = "🏆 عرض احترافي"
        elif tier == "VERIFIED" or asset.trust_score >= 80:
            market_label = "🤝 موثوق من المجتمع"
        elif views > 50:
            market_label = "⚡ نشط جداً"

        return {
            "id": asset.id,
            "title": asset.title,
            "listing_tier": tier,
            "calculated_score": score,
            "human_badge": market_label,
            "trust_indicator": "⭐⭐⭐⭐⭐" if asset.trust_score >= 85 else "⭐⭐⭐⭐" if asset.trust_score >= 70 else "⭐⭐⭐"
        }

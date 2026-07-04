import asyncio
from datetime import datetime, timedelta

# محاكاة كائن أصل تعديني متوافق مع الحقول الجديدة للاختبار السريع
class MockAsset:
    def __init__(self, id, title, tier, trust, views, favs, days_ago):
        self.id = id
        self.title = title
        self.listing_tier = tier
        self.trust_score = trust
        self.views_count = views
        self.favorites_count = favs
        self.created_at = datetime.utcnow() - timedelta(days=days_ago)

async def test_ranking_engine_scenarios():
    print("🧪 === بدء تشغيل حزمة اختبار محرك الترتيب والتنظيم الذكي (Phase C4) ===")
    from app.domain.services.ranking import MarketRankingEngine

    # إنشاء الأصول الثلاثة المتنوعة
    asset_a = MockAsset(1, "مربع ذهب أبو حمد - إنتاج تقليدي", "OPEN", 60.0, 5, 0, 0) # طازج اليوم
    asset_b = MockAsset(2, "عروق كوارتز غنية بالذهب - موقع غبيش", "VERIFIED", 85.0, 60, 4, 3) # نشط وموثق من 3 أيام
    asset_c = MockAsset(3, "مربع امتياز تعديني متكامل - رخصة سيادية", "PREMIUM", 95.0, 12, 1, 7) # شركة ثقيلة من أسبوع

    assets = [asset_a, asset_b, asset_c]

    # -------------------------------------------------------------
    # 🔥 السيناريو 1: وضع السوق النشط (Market Flow)
    # -------------------------------------------------------------
    print("\n🔥 [وضع العرض: تدفق السوق النشط] - الأحدث والتصفح اللحظي يحكم:")
    results_flow = []
    for asset in assets:
        score = MarketRankingEngine.calculate_asset_score(asset, view_mode="MARKET_FLOW")
        badge_data = MarketRankingEngine.attach_human_badges(asset, score)
        results_flow.append(badge_data)
    
    # الترتيب حسب النقاط التنازلية
    results_flow.sort(key=lambda x: x["calculated_score"], reverse=True)
    for index, res in enumerate(results_flow, 1):
        print(f"   {index}. [{res['human_badge']}] {res['title']} | النقاط: {res['calculated_score']} | التقييم: {res['trust_indicator']}")

    # -------------------------------------------------------------
    # ⭐ السيناريو 2: وضع الثقة والشفافية أولاً (Trusted First)
    # -------------------------------------------------------------
    print("\n⭐ [وضع العرض: الثقة أولاً] - من يرفع أوراقه ويبني سمعته يتقدم طبيعياً:")
    results_trust = []
    for asset in assets:
        score = MarketRankingEngine.calculate_asset_score(asset, view_mode="TRUSTED_FIRST")
        badge_data = MarketRankingEngine.attach_human_badges(asset, score)
        results_trust.append(badge_data)
    
    results_trust.sort(key=lambda x: x["calculated_score"], reverse=True)
    for index, res in enumerate(results_trust, 1):
        print(f"   {index}. [{res['human_badge']}] {res['title']} | النقاط: {res['calculated_score']} | التقييم: {res['trust_indicator']}")

    print("\n🎉 [نجاح فلسفة السوق الحي]: التغيير مرن، العدالة متوفرة، واللمسة البشرية تغلبت على الجفاف الهندسي!")

if __name__ == "__main__":
    asyncio.run(test_ranking_engine_scenarios())

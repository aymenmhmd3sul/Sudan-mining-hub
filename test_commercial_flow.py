import asyncio
import json
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.infrastructure.database import AsyncSessionLocal
from app.api.deps import get_db_session

async def test_commercial_engine():
    print("🧪 === بدء فحص المحرك التجاري ونموذج الإيرادات (Commercial MVP) ===")
    
    async with AsyncSessionLocal() as session:
        app.dependency_overrides[get_db_session] = lambda: session
        transport = ASGITransport(app=app)
        
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            
            # 1. اختبار ترقية باقة التاجر
            print("\n💳 [1. فحص ترقية حساب تاجر إلى باقة معتمد]...")
            upgrade_res = await ac.post("/commercial/trader/upgrade", json={"trader_id": 99, "target_tier": "VERIFIED"})
            print(json.dumps(upgrade_res.json(), ensure_ascii=False, indent=2))
            
            # 2. تفعيل ترويج مدفوع لإعلان البوكلين (المعرف رقم 3)
            print("\n🚀 [2. فحص دفع وترقية إعلان فردي - باقة تثبيت في الصدارة]...")
            promo_res = await ac.post("/commercial/asset/promote", json={"asset_id": 3, "promotion_type": "TOP_BOOST"})
            print(json.dumps(promo_res.json(), ensure_ascii=False, indent=2))
            
            # 3. حساب عمولة مرنة لصفقة خام ذهب بقيمة 10 مليون جنيه سوداني
            print("\n📈 [3. فحص محرك العمولات المرن - صفقة خامات]...")
            comm_res = await ac.get("/commercial/calculate-commission/raw-materials?deal_value=10000000")
            print(json.dumps(comm_res.json(), ensure_ascii=False, indent=2))
            
            # 4. لوحة الإيرادات الإدارية والمحفظة المالية للمنصة
            print("\n💼 [4. فحص لوحة الإيرادات والأرباح لمدير المنصة]...")
            rev_res = await ac.get("/commercial/admin/revenues")
            print(json.dumps(rev_res.json(), ensure_ascii=False, indent=2))
            
            # 5. استدعاء لوحة التاجر الاستشارية للبوكلين (المعرف رقم 3) لمعاينة التوصيات
            print("\n💡 [5. فحص لوحة التاجر التحفيزية الذكية والإحصاءات]...")
            trader_res = await ac.get("/commercial/trader/dashboard/3")
            print(json.dumps(trader_res.json(), ensure_ascii=False, indent=2))
            
        app.dependency_overrides.clear()

if __name__ == "__main__":
    asyncio.run(test_commercial_engine())

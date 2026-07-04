import asyncio
import json
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.infrastructure.database import AsyncSessionLocal
from app.api.deps import get_db_session

async def test_web_views_output():
    print("🧪 === بدء فحص مخرجات الـ MVP والواجهات التشغيلية ===")
    
    async with AsyncSessionLocal() as session:
        app.dependency_overrides[get_db_session] = lambda: session
        transport = ASGITransport(app=app)
        
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # 1. اختبار الصفحة الرئيسية
            print("\n🏠 [1. فحص بيانات الصفحة الرئيسية]...")
            home_res = await ac.get("/web-views/home")
            print(json.dumps(home_res.json(), ensure_ascii=False, indent=2))
            
            # 2. اختبار صفحة تفاصيل الإعلان (باستخدام معرف الإعلان 3 المتاح لدينا)
            print("\n📄 [2. فحص صفحة تفاصيل الإعلان - معرف رقم 3]...")
            detail_res = await ac.get("/web-views/asset/3")
            print(json.dumps(detail_res.json(), ensure_ascii=False, indent=2))
            
            # 3. اختبار مركز قيادة المشرف (لوحة التحكم)
            print("\n💼 [3. فحص لوحة تحكم المشرف ومركز القيادة]...")
            admin_res = await ac.get("/web-views/admin/control-center")
            print(json.dumps(admin_res.json(), ensure_ascii=False, indent=2))
            
        app.dependency_overrides.clear()

if __name__ == "__main__":
    asyncio.run(test_web_views_output())

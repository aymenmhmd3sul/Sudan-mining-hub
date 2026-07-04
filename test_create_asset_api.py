import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.infrastructure.database import AsyncSessionLocal
from app.api.deps import get_db_session

async def test_flexible_creation_flow():
    print("🧪 === بدء اختبار مسار استقبال الإعلانات المرن (API) ===")
    
    # محاكاة لبيانات قادمة من هاتف بائع (الحد الأدنى من البيانات - المبدأ الأول)
    test_payload = {
        "title": "بوكلين كوماتسو 200 للبيع في بربر",
        "category_slug": "heavy-machinery",
        "state": "ولاية نهر النيل",
        "phone_number": "0912345678",
        "primary_image_url": "https://storage.sudan-mining.com/images/poc_01.jpg"
    }
    
    # فتح جلسة قاعدة البيانات وحقنها في الـ Dependency التابع لـ FastAPI
    async with AsyncSessionLocal() as session:
        app.dependency_overrides[get_db_session] = lambda: session
        
        # التحديث الهندي لـ HTTPX 2026 باستخدام ASGITransport
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/assets/create-flexible", json=test_payload)
            
            print(f"🚦 كود الحالة المسترجع: {response.status_code}")
            
            import json
            result = response.json()
            print("✅ الاستجابة الكاملة من نظام الاستقبال المرن:")
            print(json.dumps(result, ensure_ascii=False, indent=4))
            
        app.dependency_overrides.clear()

if __name__ == "__main__":
    asyncio.run(test_flexible_creation_flow())

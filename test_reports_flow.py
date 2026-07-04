import asyncio
import json
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.infrastructure.database import AsyncSessionLocal
from app.api.deps import get_db_session

async def test_exception_moderation_flow():
    print("🧪 === بدء اختبار محرك الإدارة بالاستثناء والأتمتة الذكية ===")
    
    # استهداف الأصل رقم 3 المضاف في النظام
    target_asset_id = 3
    
    reports_payloads = [
        {"asset_id": target_asset_id, "reporter_id": 501, "reason": "رقم الهاتف لا يستجيب والبيانات تبدو وهمية"},
        {"asset_id": target_asset_id, "reporter_id": 502, "reason": "الصور مأخوذة من الإنترنت والمعدة ليست في بربر"},
        {"asset_id": target_asset_id, "reporter_id": 503, "reason": "محاولة احتيال وطلب عربون مقدم قبل المعاينة"}
    ]
    
    async with AsyncSessionLocal() as session:
        app.dependency_overrides[get_db_session] = lambda: session
        transport = ASGITransport(app=app)
        
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            for idx, payload in enumerate(reports_payloads, 1):
                print(f"\n📥 [بلاغ {idx}]: إرسال شكوى من المستخدم رقم {payload['reporter_id']}...")
                response = await ac.post("/reports/submit", json=payload)
                
                result = response.json()
                print(f"🚦 النتيجة (كود {response.status_code}):")
                print(json.dumps(result, ensure_ascii=False, indent=2))
                
        app.dependency_overrides.clear()

if __name__ == "__main__":
    asyncio.run(test_exception_moderation_flow())

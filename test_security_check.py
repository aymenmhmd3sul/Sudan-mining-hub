import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.asset_state import AssetStateService

async def test_security_violation():
    print("🛡️ === بدء اختبار اختراق الأمان (Security Guard Test) ===")
    
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        state_service = AssetStateService(repo)
        
        # 1. إنشاء أصل مع بيانات موقع تجريبية صالحة (الولاية: ولاية نهر النيل)
        asset_data = {
            "title": "أصل محمي أمنياً", 
            "description": "اختبار فحص الصلاحيات والملكية", 
            "category_id": 1, 
            "seller_id": 5001, 
            "status": "DRAFT"
        }
        location_data = {
            "state": "ولاية نهر النيل",
            "region": "بربر"
        }
        
        new_asset = await repo.create_asset_with_details(asset_data, location_data, [])
        await session.commit()
        asset_id = new_asset.id
        
        print(f"✅ تم حفظ الأصل رقم [{asset_id}] بنجاح للمالك رقم 5001")
        
        # 2. محاولة الاختراق: مستخدم آخر (9999) يحاول تعديل حالة هذا الأصل
        print(f"\n🚫 محاولة الاختراق: مستخدم غريب (ID: 9999) يحاول دفع الأصل إلى [PENDING_REVIEW]...")
        
        success, message = await state_service.transition_status(
            asset_id=asset_id,
            to_state="PENDING_REVIEW",
            actor="Hacker_User",
            actor_id="9999", 
            role="SELLER",
            reason="محاولة تعديل غير مشروعة"
        )
        
        if not success:
            print(f"\n🎉 [نجاح باهر للحارس الأمني]: تم صد المحاولة بنجاح! الرد: {message}")
        else:
            print("\n❌ [ثغرة خطيرة]: النظام سمح للمخترق بتجاوز الصلاحيات!")

if __name__ == "__main__":
    asyncio.run(test_security_violation())

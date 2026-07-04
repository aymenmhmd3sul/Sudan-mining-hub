import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.asset_state import AssetStateService
from app.domain.services.security import SecurityGuard

async def run_advanced_security_scenarios():
    print("🛡️ === بدء اختبار طبقة التفويض الموحدة والأحداث الأمنية ===")
    
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        state_service = AssetStateService(repo)
        
        # 1. إنشاء أصل يملكه البائع رقم 6006 (حالة مسودة DRAFT)
        asset_data = {"title": "مربع تعدين محمي مركزيًا", "description": "مربع للاختبار الأمني الشامل", "category_id": 1, "seller_id": 6006, "status": "DRAFT"}
        location_data = {"state": "ولاية البحر الأحمر", "region": "جبيت"}
        
        asset = await repo.create_asset_with_details(asset_data, location_data, [])
        await session.commit()
        print(f"✅ تم حفظ الأصل رقم [{asset.id}] بنجاح للمالك 6006")
        
        # السيناريو أ: محاولة بائع غريب (7007) تعديل حالة الأصل
        print("\n🚫 [فحص اختراق]: محاولة مستخدم غريب تعديل حالة الأصل...")
        success, msg = await state_service.transition_status(
            asset_id=asset.id, to_state="PENDING_REVIEW", actor="Malicious_User", actor_id="7007", role="SELLER"
        )
        print(f"🔒 النتيجة: مسموح؟ {success} | الرسالة: {msg}")

        # السيناريو ب: فحص قاعدة عمل التفاوض (البائع يشتري أصله)
        print("\n🚫 [فحص قاعدة العمل]: محاولة البائع (6006) بدء تفاوض بصفة مشتري على أصله الخاص...")
        allowed, n_msg = await SecurityGuard.authorize_action(
            db_session=session, action="CREATE_NEGOTIATION", actor_id="6006", actor_name="Seller_Ayman", role="BUYER", asset=asset
        )
        print(f"🔒 النتيجة: مسموح؟ {allowed} | الرسالة: {n_msg}")
        
        # السيناريو ج: فحص التفاوض على أصل غير منشور (DRAFT)
        print("\n🚫 [فحص قاعدة العمل]: محاولة مشتري حقيقي التفاوض على أصل ما زال مسودة (DRAFT)...")
        allowed_b, b_msg = await SecurityGuard.authorize_action(
            db_session=session, action="CREATE_NEGOTIATION", actor_id="8888", actor_name="True_Buyer", role="BUYER", asset=asset
        )
        print(f"🔒 النتيجة: مسموح؟ {allowed_b} | الرسالة: {b_msg}")

if __name__ == "__main__":
    asyncio.run(run_advanced_security_scenarios())

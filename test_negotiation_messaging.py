import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.negotiation import NegotiationService
from app.domain.services.asset_state import AssetStateService

async def run_messaging_suite():
    print("🧪 === بدء تشغيل حزمة اختبار محرك المراسلات والنزاهة القانونية (Phase 3) ===")
    
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        neg_service = NegotiationService(session, repo)
        state_service = AssetStateService(repo)
        
        # 1. إعداد مربع تعدين معتمد
        asset_data = {"title": "عرق ذهب مرو - أبو حمد", "description": "خامات عالية الجودة", "category_id": 1, "seller_id": 5001, "status": "DRAFT"}
        location_data = {"state": "ولاية نهر النيل", "region": "أبو حمد"}
        asset = await repo.create_asset_with_details(asset_data, location_data, [])
        await session.commit()
        
        await state_service.transition_status(asset.id, "PENDING_REVIEW", "Seller_5001", "5001", "SELLER")
        await state_service.transition_status(asset.id, "APPROVED", "Admin_Inspector", "99", "ADMIN")
        await session.commit()
        
        # 2. فتح جلسة تفاوض للمشتري (2002)
        _, _, negotiation = await neg_service.start_negotiation(asset.id, buyer_id="2002", role="BUYER")
        await session.commit()
        print(f"📌 تم تفعيل جلسة التفاوض رقم [{negotiation.id}]")

        # -------------------------------------------------------------
        # 🛠️ اختبار 1: تبادل رسائل شرعي بين المشتري والبائع
        # -------------------------------------------------------------
        ok_m1, msg1 = await neg_service.send_message(negotiation.id, sender_id="2002", role="BUYER", text="السلام عليكم، هل السعر قابل للتفاوض؟")
        ok_m2, msg2 = await neg_service.send_message(negotiation.id, sender_id="5001", role="SELLER", text="وعليكم السلام، نعم بحدود معقولة.")
        print(f"- إرسال المشتري: {ok_m1} | إرسال البائع: {ok_m2}")

        # -------------------------------------------------------------
        # 🛠️ اختبار 2: منع مستخدم متسلل (9999) من إرسال أو قراءة الرسائل
        # -------------------------------------------------------------
        bad_send, bad_send_msg = await neg_service.send_message(negotiation.id, sender_id="9999", role="BUYER", text="محاولة حقن رسالة")
        bad_list, _, _ = await neg_service.list_messages(negotiation.id, user_id="9999", role="BUYER")
        print(f"- صد اختراق الإرسال الخارجي: {not bad_send} | صد اختراق التجسس: {not bad_list}")

        # -------------------------------------------------------------
        # 🛠️ اختبار 3: التحقق من عمل الـ Pagination والترتيب
        # -------------------------------------------------------------
        await neg_service.send_message(negotiation.id, sender_id="2002", role="BUYER", text="سأقدم عرضاً بـ 50 ألف دولار")
        _, _, chat_list = await neg_service.list_messages(negotiation.id, user_id="2002", role="BUYER", limit=2, offset=0)
        print(f"- فحص الـ Pagination (جلب رسالتين فقط): تم جلب [{len(chat_list)}] رسالة.")

        # -------------------------------------------------------------
        # 🛠️ اختبار 4: close_chat حظر المراسلة التلقائي بعد قبول الصفقات
        # -------------------------------------------------------------
        print("\n💰 [محاكاة]: البائع يقبل العرض المالي ويغلق الصفقة حكماً...")
        await neg_service.create_offer(negotiation.id, amount=50000.0, actor_id="2002", role="BUYER")
        await neg_service.accept_offer(negotiation.id, asset_state_service=state_service, actor_id="5001", role="SELLER")
        await session.commit()

        # محاولة إرسال رسالة جديدة بعد الإغلاق
        post_close_send, post_close_msg = await neg_service.send_message(negotiation.id, sender_id="2002", role="BUYER", text="هل يمكنني الاتصال بك الآن؟")
        print(f"- منع المراسلة بعد الإغلاق الحتمي: {not post_close_send} | الرد: {post_close_msg}")

if __name__ == "__main__":
    asyncio.run(run_messaging_suite())

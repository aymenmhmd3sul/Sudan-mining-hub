import os
import sys
from datetime import datetime
from app.database import SessionLocal
from app.models.user import User
from app.models.market_core import AssetItem, MarketListing
from app.models.investor_core import InvestorProfile, LetterOfIntent
from app.models.negotiation import MarketDeal

# 1. التحقق الصارم من بيئة التشغيل لحماية الإنتاج
if os.getenv("SEED_DEMO_DATA") != "true":
    print("❌ خطأ أمني: لم يتم تفعيل بيئة التغذية التجريبية.")
    print("برجاء تشغيل السكريبت هكذا: SEED_DEMO_DATA=true python seed_dashboard_data.py")
    sys.exit(1)

db = SessionLocal()

try:
    print("⏳ بدء معاملة حقن البيانات التجريبية الموحدة (Atomic Transaction)...")
    
    # 2. جلب أو إنشاء مستخدمين حقيقيين لتجنب كسر الـ Foreign Keys
    test_user = db.query(User).filter(User.email == "test@mining.com").first()
    if not test_user:
        test_user = User(email="test@mining.com", username="test_miner")
        db.add(test_user)
        db.flush() # جلب الـ ID دون عمل Commit

    buyer_user = db.query(User).filter(User.email == "buyer@mining.com").first()
    if not buyer_user:
        buyer_user = User(email="buyer@mining.com", username="sudan_buyer")
        db.add(buyer_user)
        db.flush()

    # 3. تغذية المستثمرين (Idempotent: نتحقق بالاسم لمنع التكرار)
    investors_data = [
        {"company_name": "شركة التعدين العربية", "country": "السودان", "contact_info": "info@arabmining.sd", "is_verified": True},
        {"company_name": "Gold Coast Investors", "country": "الإمارات", "contact_info": "invest@goldcoast.ae", "is_verified": True},
        {"company_name": "مجموعة النيل للاستثمار", "country": "السودان", "contact_info": "nile@mining.sd", "is_verified": False}
    ]
    
    created_investors = []
    for inv in investors_data:
        existing = db.query(InvestorProfile).filter(InvestorProfile.company_name == inv["company_name"]).first()
        if not existing:
            existing = InvestorProfile(**inv)
            db.add(existing)
            db.flush()
        created_investors.append(existing)

    # 4. تغذية الأصول والطلبات في السوق (AssetItem & MarketListing)
    # أصل 1: ذهب خام نشط ومحقق
    if not db.query(AssetItem).filter(AssetItem.title == "شحنة ذهب خام - أبوحمد").first():
        asset_1 = AssetItem(owner_id=test_user.id, asset_type="RAW_GOLD", title="شحنة ذهب خام - أبوحمد", quantity=500.0, unit="GRAM")
        db.add(asset_1)
        db.flush()
        
        listing_1 = MarketListing(asset_id=asset_1.id, publisher_id=test_user.id, price=35000.0, currency="USD", status="OPEN", is_verified_by_agent=True)
        db.add(listing_1)

    # أصل 2: معدات معلقة قيد التحقق (status='PENDING' أو غير محققة)
    if not db.query(AssetItem).filter(AssetItem.title == "كسارة غربال إنتاجية عالية").first():
        asset_2 = AssetItem(owner_id=test_user.id, asset_type="EQUIPMENT", title="كسارة غربال إنتاجية عالية", quantity=1.0, unit="PIECE")
        db.add(asset_2)
        db.flush()
        
        listing_2 = MarketListing(asset_id=asset_2.id, publisher_id=test_user.id, price=120000.0, currency="USD", status="PENDING", is_verified_by_agent=False)
        db.add(listing_2)

    # 5. تغذية غرف المفاوضات والصفقات الحية (MarketDeal)
    # سنتحقق من وجود صفقة بين البائع والمشتري لنفس الأصول منعاً للتكرار
    existing_deal = db.query(MarketDeal).filter(MarketDeal.seller_id == test_user.id, MarketDeal.buyer_id == buyer_user.id).first()
    if not existing_deal:
        deal = MarketDeal(
            asset_id=1, # نمرر معرف افتراضي يتوافق مع جدول mining_assets
            seller_id=test_user.id,
            buyer_id=buyer_user.id,
            status="OPEN"
        )
        db.add(deal)

    # 6. تغذية خطابات النوايا (LetterOfIntent)
    if created_investors:
        existing_loi = db.query(LetterOfIntent).filter(LetterOfIntent.investor_id == created_investors[0].id).first()
        if not existing_loi:
            loi = LetterOfIntent(
                investor_id=created_investors[0].id,
                asset_id=1,
                status="Submitted",
                notes="رغبة جادة في الاستحواذ على حصة إنتاجية"
            )
            db.add(loi)

    # حفظ كل العمليات ككتلة واحدة آمنة
    db.commit()
    print("✅ تم حقن البيانات وتغذيتها بنجاح تام وبشكل Idempotent!")

except Exception as e:
    db.rollback()
    print(f"❌ تراجع (Rollback): حدث خطأ أثناء التغذية ولم يتأثر النظام: {e}")
finally:
    db.close()

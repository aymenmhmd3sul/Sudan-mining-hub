from app.database import SessionLocal
from app.services.finance_service import FinanceService
from app.models.bank import Bank

def run_test():
    db = SessionLocal()
    try:
        finance = FinanceService(db)
        
        print("--- بدء اختبار النظام المالي ---")
        
        # 1. اختبار العملات
        print("\n1. جاري اختبار إضافة/تحديث العملة...")
        currency = finance.add_or_update_currency(code="USD", name="US Dollar", rate=72500.0)
        print(f"✅ تم حفظ العملة: {currency.code} | السعر: {currency.rate_to_base}")
        
        # 2. اختبار جلب السعر
        rate = finance.get_exchange_rate("USD")
        print(f"✅ تم استدعاء السعر بنجاح: {rate}")
        
        # 3. اختبار البنوك
        print("\n2. جاري اختبار إضافة بنك...")
        existing_bank = db.query(Bank).filter(Bank.name == "Central Bank of Sudan").first()
        if not existing_bank:
            new_bank = Bank(
                name="Central Bank of Sudan", 
                swift_code="CBSDSD", 
                is_active=True, 
                config={"type": "central", "api_status": "mock"}
            )
            db.add(new_bank)
            db.commit()
            print("✅ تم إنشاء البنك بنجاح.")
        else:
            print("✅ البنك موجود مسبقاً.")
            
        # 4. اختبار جلب البنوك النشطة
        banks = finance.get_active_banks()
        print(f"✅ عدد البنوك النشطة التي تم العثور عليها: {len(banks)}")
        for b in banks:
            print(f"   🏦 {b.name} (SWIFT: {b.swift_code})")
            
        print("\n🚀 اكتمل الاختبار: النظام المالي يعمل بكفاءة تامة!")
        
    except Exception as e:
        print(f"\n❌ فشل الاختبار: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_test()

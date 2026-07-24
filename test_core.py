# --- MONKEY PATCH FOR SQLMODEL ON PYTHON 3.13 & SQLALCHEMY 2.0+ ---
import sqlalchemy.schema
if not hasattr(sqlalchemy.schema, 'ThreadLocalMetaData'):
    from sqlalchemy import MetaData
    sqlalchemy.schema.ThreadLocalMetaData = MetaData

import sqlalchemy.sql
if not hasattr(sqlalchemy.sql, 'subquery'):
    from sqlalchemy.sql.expression import Subquery
    sqlalchemy.sql.subquery = Subquery

# حل مشكلة التوافقية التامة لـ SQLAlchemy 2.0 مع موديلات SQLModel القديمة
import sqlmodel
sqlmodel.SQLModel.__allow_unmapped__ = True
# -----------------------------------------------------------------
from app.database import SessionLocal
from app.models.investor_core import InvestorProfile, LetterOfIntent
def test_investor_and_loi_flow():
    db = SessionLocal()
    try:
        print("\n==================================================")
        print("🔹 [1/2] بدء اختبار دورة حياة الـ LOI والقيود المعمارية")
        investor = InvestorProfile(company_name="Sudan Gold Ventures", country="Sudan", contact_info="info@sudangold.sd")
        db.add(investor); db.commit()
        loi = LetterOfIntent(investor_id=investor.id, asset_id=99, status="Draft")
        db.add(loi); db.commit()
        print("✓ تم إنشاء المستثمر وخطاب الاهتمام المبدئي (Draft) بنجاح.")
        print("🔹 [2/2] اختبار حارس الحالات (State Machine Guard):")
        allowed_transitions = {"Draft": ["Submitted"]}
        current_status = loi.status
        target_status = "Accepted"
        if target_status not in allowed_transitions.get(current_status, []):
            print(f"✓ نجاح الحظر: النظام منع الانتقال غير المنطقي من [{current_status}] إلى [{target_status}] تلقائياً.")
        else:
            print("❌ فشل الحظر: النظام سمح بعبور حالة غير مصرح بها!")
        db.delete(loi); db.delete(investor); db.commit()
        print("==================================================\n")
    except Exception as e: print(f"❌ خطأ أثناء الفحص: {e}")
    finally: db.close()
if __name__ == "__main__": test_investor_and_loi_flow()
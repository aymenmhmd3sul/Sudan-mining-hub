import os
import sys
# إضافة مسار المشروع لجذر الاستيراد
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlmodel import SQLModel, create_engine, Session
from app.models.finance import Invoice, Escrow
from decimal import Decimal

# إعداد قاعدة البيانات
sqlite_url = "sqlite:///test_database.db"
engine = create_engine(sqlite_url)

# إنشاء الجداول
SQLModel.metadata.create_all(engine)

# اختبار الإضافة
with Session(engine) as session:
    invoice = Invoice(
        opportunity_id=1, buyer_id=10, seller_id=20, 
        invoice_number="INV-001", total_amount=Decimal("1000.00")
    )
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    
    escrow = Escrow(invoice_id=invoice.id, amount=Decimal("1000.00"))
    session.add(escrow)
    session.commit()
    
    session.refresh(invoice)
    print(f"Test Successful: Invoice {invoice.invoice_number} created with Escrow ID {invoice.escrow.id}")

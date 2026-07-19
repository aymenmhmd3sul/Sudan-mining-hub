from sqlalchemy.orm import Session
from app.models.currency import Currency
from app.models.bank import Bank

class FinanceService:
    def __init__(self, db: Session):
        self.db = db

    def get_active_banks(self):
        """جلب قائمة البنوك المفعلة حالياً في المنصة"""
        return self.db.query(Bank).filter(Bank.is_active == True).all()

    def get_exchange_rate(self, currency_code: str):
        """جلب سعر الصرف لعملة محددة"""
        currency = self.db.query(Currency).filter(Currency.code == currency_code).first()
        if currency:
            return currency.rate_to_base
        return None

    def add_or_update_currency(self, code: str, name: str, rate: float):
        """تحديث أو إضافة عملة جديدة (يستخدمها المشرف)"""
        currency = self.db.query(Currency).filter(Currency.code == code).first()
        if currency:
            currency.rate_to_base = rate
        else:
            currency = Currency(code=code, name=name, rate_to_base=rate)
            self.db.add(currency)
        self.db.commit()
        self.db.refresh(currency)
        return currency

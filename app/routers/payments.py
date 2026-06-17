from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime, timedelta

router = APIRouter()
TRANSACTIONS_FILE = "data/transactions.json"
OPPORTUNITIES_FILE = "data/opportunities.json"
OFFERS_FILE = "data/offers.json"

os.makedirs("data", exist_ok=True)

if not os.path.exists(TRANSACTIONS_FILE):
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump([], f)

def get_opportunities():
    with open(OPPORTUNITIES_FILE, "r") as f:
        return json.load(f)

def save_opportunities(data):
    with open(OPPORTUNITIES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_offers():
    with open(OFFERS_FILE, "r") as f:
        return json.load(f)

def get_transactions():
    with open(TRANSACTIONS_FILE, "r") as f:
        return json.load(f)

def save_transactions(data):
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@router.get("/commission/{opportunity_id}")
def calculate_commission(opportunity_id: int):
    """
    حساب العمولة بناءً على نوع المعدات في الطلب
    """
    opportunities = get_opportunities()
    opp = None
    for o in opportunities:
        if o["id"] == opportunity_id:
            opp = o
            break
    if not opp:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    
    opp_type = opp.get("type", "light_equipment")
    
    commission_fixed = None
    commission_percentage = None
    commission_text = ""
    
    if opp_type == "light_equipment":
        commission_fixed = 100000  # 100,000 ج.س
        commission_text = "100,000 ج.س (عمولة ثابتة)"
    elif opp_type == "heavy_equipment":
        commission_percentage = 0.25  # 0.25%
        commission_text = "0.25% من قيمة الصفقة"
    else:
        commission_fixed = 50000  # قيمة افتراضية للأنواع الأخرى
        commission_text = "50,000 ج.س (عمولة افتراضية)"
    
    # جلب سعر العرض المختار إن وجد
    final_price = None
    if opp.get("selected_offer_id"):
        offers = get_offers()
        for of in offers:
            if of["id"] == opp["selected_offer_id"]:
                final_price = of["price"]
                break
    
    return {
        "opportunity_id": opportunity_id,
        "commission_fixed": commission_fixed,
        "commission_percentage": commission_percentage,
        "commission_text": commission_text,
        "final_price": final_price,
        "bank_account": "🏦 Sudan Mining Hub - Bank of Khartoum - Account: 123456789 (يرجى إيداع العمولة في هذا الحساب)"
    }

@router.post("/confirm-delivery/{opportunity_id}")
def confirm_delivery(opportunity_id: int, user_id: int):
    """
    تأكيد الاستلام من أحد الطرفين (المشتري أو التاجر)
    """
    opportunities = get_opportunities()
    opp = None
    for o in opportunities:
        if o["id"] == opportunity_id:
            opp = o
            break
    if not opp:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    
    if opp["status"] != "agreed":
        raise HTTPException(status_code=400, detail="لا يمكن تأكيد الاستلام إلا بعد الاتفاق")
    
    # تغيير الحالة إلى مكتمل
    opp["status"] = "completed"
    save_opportunities(opportunities)
    
    # حساب العمولة
    commission_data = calculate_commission(opportunity_id)
    
    # حفظ المعاملة
    transactions = get_transactions()
    new_trans = {
        "id": len(transactions) + 1,
        "opportunity_id": opportunity_id,
        "commission_fixed": commission_data.get("commission_fixed"),
        "commission_percentage": commission_data.get("commission_percentage"),
        "final_price": commission_data.get("final_price"),
        "confirmed_by": user_id,
        "confirmed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending_payment"
    }
    transactions.append(new_trans)
    save_transactions(transactions)
    
    return {
        "status": "success",
        "message": "✅ تم تأكيد الاستلام. يجب على التاجر دفع العمولة الآن.",
        "commission_details": commission_data,
        "bank_account": "🏦 Sudan Mining Hub - Bank of Khartoum - Account: 123456789"
    }

@router.get("/subscription/{seller_id}")
def get_subscription(seller_id: int):
    """
    التحقق من اشتراك التاجر وعرض رقم الحساب للدفع
    """
    users_file = "data/users.json"
    if not os.path.exists(users_file):
        raise HTTPException(status_code=404, detail="لا يوجد مستخدمون")
    with open(users_file, "r") as f:
        users = json.load(f)
    
    for u in users:
        if u["id"] == seller_id and u["role"] == "seller":
            if u.get("is_active", False):
                return {
                    "status": "active",
                    "subscription_end": u.get("subscription_end"),
                    "message": "✅ اشتراكك نشط"
                }
            else:
                return {
                    "status": "inactive",
                    "message": "❌ اشتراكك غير نشط. يرجى دفع 3,000 ج.س شهرياً",
                    "bank_account": "🏦 Sudan Mining Hub - Bank of Khartoum - Account: 123456789 (للاشتراك الشهري)"
                }
    raise HTTPException(status_code=404, detail="المستخدم غير موجود أو ليس تاجراً")

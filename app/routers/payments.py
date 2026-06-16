from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import json
import os
from datetime import datetime, timedelta

router = APIRouter()
TRANSACTIONS_FILE = "data/transactions.json"
SUBSCRIPTIONS_FILE = "data/subscriptions.json"
USERS_FILE = "data/users.json"

if not os.path.exists(TRANSACTIONS_FILE):
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump([], f)
if not os.path.exists(SUBSCRIPTIONS_FILE):
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump([], f)

def get_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_transactions():
    with open(TRANSACTIONS_FILE, "r") as f:
        return json.load(f)

def save_transactions(data):
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@router.post("/commission/{opportunity_id}")
def calculate_commission(opportunity_id: int):
    """
    حساب العمولة بناءً على نوع المعدات
    """
    # في الواقع سنجلب تفاصيل الفرصة من ملف الفرص
    # لكن هنا نستخدم منطقاً مبسطاً
    opportunity_type = "light_equipment"  # سيتم جلبها من قاعدة البيانات
    
    commission_fixed = None
    commission_percentage = None
    
    if opportunity_type == "light_equipment":
        commission_fixed = 100000  # 100,000 ج.س
    elif opportunity_type == "heavy_equipment":
        commission_percentage = 0.25  # 0.25%
    else:
        commission_fixed = 50000  # قيمة افتراضية
    
    return {
        "opportunity_id": opportunity_id,
        "commission_fixed": commission_fixed,
        "commission_percentage": commission_percentage,
        "bank_account": "Sudan Mining Hub - Bank of Khartoum - Account: 123456789"
    }

@router.post("/confirm-delivery/{opportunity_id}")
def confirm_delivery(opportunity_id: int, user_id: int):
    """
    تأكيد الاستلام من أحد الطرفين
    """
    transactions = get_transactions()
    # نبحث عن صفقة مفتوحة
    for t in transactions:
        if t["opportunity_id"] == opportunity_id and t["status"] == "pending":
            t["status"] = "completed"
            t["confirmed_by"] = user_id
            t["confirmed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_transactions(transactions)
            return {
                "status": "success",
                "message": "تم تأكيد الاستلام، يمكن الآن دفع العمولة",
                "commission": t.get("commission", 0)
            }
    
    # إذا لم توجد صفقة، ننشئ واحدة
    new_transaction = {
        "id": len(transactions) + 1,
        "opportunity_id": opportunity_id,
        "commission": 100000,  # مثال
        "status": "pending",
        "confirmed_by": user_id,
        "confirmed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    transactions.append(new_transaction)
    save_transactions(transactions)
    return {
        "status": "success",
        "message": "تم تأكيد الاستلام",
        "commission": 100000
    }

@router.get("/subscription/{seller_id}")
def get_subscription(seller_id: int):
    """
    التحقق من اشتراك التاجر
    """
    users = get_users()
    for u in users:
        if u["id"] == seller_id and u["role"] == "seller":
            if u.get("is_active", False):
                return {"status": "active", "subscription_end": u.get("subscription_end")}
            else:
                return {
                    "status": "inactive",
                    "message": "اشتراكك غير نشط، يرجى دفع 3,000 ج.س شهرياً",
                    "bank_account": "Sudan Mining Hub - Bank of Khartoum - Account: 123456789"
                }
    raise HTTPException(status_code=404, detail="المستخدم غير موجود")

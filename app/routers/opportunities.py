from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime

router = APIRouter()
OPPORTUNITIES_FILE = "data/opportunities.json"
OFFERS_FILE = "data/offers.json"
USERS_FILE = "data/users.json"

os.makedirs("data", exist_ok=True)

if not os.path.exists(OPPORTUNITIES_FILE):
    with open(OPPORTUNITIES_FILE, "w") as f:
        json.dump([], f)
if not os.path.exists(OFFERS_FILE):
    with open(OFFERS_FILE, "w") as f:
        json.dump([], f)

class OpportunityCreate(BaseModel):
    buyer_id: int
    type: str
    specs: str
    budget: float
    location: str
    city: str

class OfferCreate(BaseModel):
    opportunity_id: int
    seller_id: int
    price: float
    specs: str
    delivery_time: str
    condition: str  # new, used

def get_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def get_opportunities():
    with open(OPPORTUNITIES_FILE, "r") as f:
        return json.load(f)

def save_opportunities(data):
    with open(OPPORTUNITIES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_offers():
    with open(OFFERS_FILE, "r") as f:
        return json.load(f)

def save_offers(data):
    with open(OFFERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@router.post("/create")
def create_opportunity(opp: OpportunityCreate):
    opportunities = get_opportunities()
    new_opp = {
        "id": len(opportunities) + 1,
        **opp.dict(),
        "status": "open",  # open, negotiating, agreed, completed
        "buyer_confirmed": False,
        "seller_confirmed": False,
        "selected_offer_id": None,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    opportunities.append(new_opp)
    save_opportunities(opportunities)
    return {"status": "success", "opportunity": new_opp}

@router.get("/list")
def list_opportunities():
    return {"opportunities": get_opportunities()}

@router.get("/all-offers")
def list_all_offers():
    return {"offers": get_offers()}

@router.get("/{opp_id}")
def get_opportunity(opp_id: int):
    opportunities = get_opportunities()
    for opp in opportunities:
        if opp["id"] == opp_id:
            return {"opportunity": opp}
    raise HTTPException(status_code=404, detail="الطلب غير موجود")

@router.post("/offer")
def create_offer(offer: OfferCreate):
    # التحقق من اشتراك التاجر
    users = get_users()
    seller = None
    for u in users:
        if u["id"] == offer.seller_id:
            seller = u
            break
    if not seller:
        raise HTTPException(status_code=404, detail="التاجر غير موجود")
    if seller.get("role") != "seller":
        raise HTTPException(status_code=403, detail="هذا المستخدم ليس تاجراً")
    if not seller.get("is_active", False):
        raise HTTPException(
            status_code=403,
            detail="اشتراكك غير نشط. يرجى دفع 3,000 ج.س شهرياً لتفعيل حسابك. رقم الحساب: Sudan Mining Hub - Bank of Khartoum - Account: 123456789"
        )
    
    # التحقق من أن الطلب ما زال مفتوحاً
    opportunities = get_opportunities()
    opp_exists = False
    for opp in opportunities:
        if opp["id"] == offer.opportunity_id and opp["status"] == "open":
            opp_exists = True
            break
    if not opp_exists:
        raise HTTPException(status_code=400, detail="هذا الطلب غير متاح للعروض (مغلق أو مكتمل)")
    
    offers = get_offers()
    new_offer = {
        "id": len(offers) + 1,
        **offer.dict(),
        "status": "pending",  # pending, accepted, rejected
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    offers.append(new_offer)
    save_offers(offers)
    return {"status": "success", "offer": new_offer}

@router.get("/offers/{opportunity_id}")
def get_offers_for_opportunity(opportunity_id: int):
    offers = get_offers()
    result = [o for o in offers if o["opportunity_id"] == opportunity_id]
    return {"offers": result}

# نقطة نهاية لتأكيد الاتفاق (يضغطها المشتري أو التاجر)
@router.post("/confirm-agreement/{opportunity_id}/{user_id}")
def confirm_agreement(opportunity_id: int, user_id: int):
    opportunities = get_opportunities()
    opp = None
    for o in opportunities:
        if o["id"] == opportunity_id:
            opp = o
            break
    if not opp:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    
    users = get_users()
    user = None
    for u in users:
        if u["id"] == user_id:
            user = u
            break
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    
    if user["role"] == "buyer":
        opp["buyer_confirmed"] = True
    elif user["role"] == "seller":
        opp["seller_confirmed"] = True
    else:
        raise HTTPException(status_code=403, detail="دور غير معروف")
    
    # إذا وافق الطرفان، نغلق الطلب ونغير الحالة
    if opp["buyer_confirmed"] and opp["seller_confirmed"]:
        opp["status"] = "agreed"
        # نحدد العرض المختار (آخر عرض أو الأقل سعراً - مبسط)
        offers = get_offers()
        best_offer = None
        for of in offers:
            if of["opportunity_id"] == opportunity_id and of["status"] == "pending":
                if best_offer is None or of["price"] < best_offer["price"]:
                    best_offer = of
        if best_offer:
            opp["selected_offer_id"] = best_offer["id"]
            # تحديث حالة العرض إلى مقبول
            for of in offers:
                if of["id"] == best_offer["id"]:
                    of["status"] = "accepted"
                    break
            save_offers(offers)
    
    save_opportunities(opportunities)
    return {
        "status": "success",
        "opportunity": opp,
        "message": "تم تأكيد الاتفاق" if opp["buyer_confirmed"] and opp["seller_confirmed"] else "تم تأكيد موافقتك، في انتظار الطرف الآخر"
    }

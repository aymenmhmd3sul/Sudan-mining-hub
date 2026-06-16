from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import json
import os
from datetime import datetime, timedelta

router = APIRouter()
USERS_FILE = "data/users.json"
ADS_FILE = "data/ads.json"
GOLD_PRICES_FILE = "data/gold_prices.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)
if not os.path.exists(ADS_FILE):
    with open(ADS_FILE, "w") as f:
        json.dump([], f)
if not os.path.exists(GOLD_PRICES_FILE):
    with open(GOLD_PRICES_FILE, "w") as f:
        json.dump([], f)

def get_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

@router.get("/users")
def list_users():
    return {"users": get_users()}

@router.post("/activate-seller/{seller_id}")
def activate_seller(seller_id: int):
    users = get_users()
    for u in users:
        if u["id"] == seller_id:
            u["is_active"] = True
            u["subscription_end"] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
            save_users(users)
            return {"status": "success", "message": "تم تفعيل حساب التاجر"}
    raise HTTPException(status_code=404, detail="المستخدم غير موجود")

@router.post("/deactivate-seller/{seller_id}")
def deactivate_seller(seller_id: int):
    users = get_users()
    for u in users:
        if u["id"] == seller_id:
            u["is_active"] = False
            save_users(users)
            return {"status": "success", "message": "تم إلغاء اشتراك التاجر"}
    raise HTTPException(status_code=404, detail="المستخدم غير موجود")

# إدارة الإعلانات
class AdCreate(BaseModel):
    title_ar: str
    title_en: str
    image_url: str
    link: str
    position: str  # top, sidebar, bottom

@router.post("/ad")
def create_ad(ad: AdCreate):
    ads = []
    if os.path.exists(ADS_FILE):
        with open(ADS_FILE, "r") as f:
            ads = json.load(f)
    new_ad = {
        "id": len(ads) + 1,
        **ad.dict(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ads.append(new_ad)
    with open(ADS_FILE, "w") as f:
        json.dump(ads, f, indent=2)
    return {"status": "success", "ad": new_ad}

# إدارة أسعار الذهب المحلية
class GoldPriceCreate(BaseModel):
    city: str
    price_gram: float
    price_ounce: float

@router.post("/gold-price")
def set_gold_price(gp: GoldPriceCreate):
    prices = []
    if os.path.exists(GOLD_PRICES_FILE):
        with open(GOLD_PRICES_FILE, "r") as f:
            prices = json.load(f)
    
    # تحديث السعر للمدينة إذا كانت موجودة
    for p in prices:
        if p["city"] == gp.city:
            p["price_gram"] = gp.price_gram
            p["price_ounce"] = gp.price_ounce
            p["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(GOLD_PRICES_FILE, "w") as f:
                json.dump(prices, f, indent=2)
            return {"status": "success", "message": f"تم تحديث سعر الذهب في {gp.city}"}
    
    # إذا لم توجد المدينة، نضيفها
    new_price = {
        **gp.dict(),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    prices.append(new_price)
    with open(GOLD_PRICES_FILE, "w") as f:
        json.dump(prices, f, indent=2)
    return {"status": "success", "message": f"تم إضافة سعر الذهب في {gp.city}"}

@router.get("/gold-prices")
def get_gold_prices():
    if os.path.exists(GOLD_PRICES_FILE):
        with open(GOLD_PRICES_FILE, "r") as f:
            return {"prices": json.load(f)}
    return {"prices": []}

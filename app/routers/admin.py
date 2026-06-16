from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import json
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

router = APIRouter()
USERS_FILE = "data/users.json"
ADS_FILE = "data/ads.json"
GOLD_PRICES_FILE = "data/gold_prices.json"
UPLOAD_DIR = "app/static/uploads"

os.makedirs("data", exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

# ================== الإعلانات الجديدة (مع رفع الصور) ==================
@router.post("/ad")
async def create_ad(
    title_ar: str = Form(...),
    title_en: str = Form(...),
    description: str = Form(...),
    link: str = Form(...),
    position: str = Form(...),
    status: str = Form(...),  # published, draft
    image_file: UploadFile = File(None),
    image_url: str = Form(None)  # رابط احتياطي
):
    # حفظ الصورة إذا تم رفعها
    saved_image_path = None
    if image_file and image_file.filename:
        # تحديد اسم ملف آمن
        file_extension = os.path.splitext(image_file.filename)[1]
        safe_filename = f"ad_{datetime.now().strftime('%Y%m%d%H%M%S')}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
        
        saved_image_path = f"/static/uploads/{safe_filename}"
    
    # استخدام الرابط الاحتياطي إذا لم يتم رفع صورة
    final_image_url = saved_image_path if saved_image_path else image_url
    
    if not final_image_url:
        raise HTTPException(status_code=400, detail="يرجى إما رفع صورة أو إدخال رابط صورة")
    
    ads = []
    if os.path.exists(ADS_FILE):
        with open(ADS_FILE, "r") as f:
            ads = json.load(f)
    
    new_ad = {
        "id": len(ads) + 1,
        "title_ar": title_ar,
        "title_en": title_en,
        "description": description,
        "image_url": final_image_url,
        "link": link,
        "position": position,
        "status": status,  # published أو draft
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ads.append(new_ad)
    with open(ADS_FILE, "w") as f:
        json.dump(ads, f, indent=2)
    return {"status": "success", "ad": new_ad}

@router.get("/ads")
def get_ads():
    if os.path.exists(ADS_FILE):
        with open(ADS_FILE, "r") as f:
            return {"ads": json.load(f)}
    return {"ads": []}

# ================== أسعار الذهب ==================
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
    
    for p in prices:
        if p["city"] == gp.city:
            p["price_gram"] = gp.price_gram
            p["price_ounce"] = gp.price_ounce
            p["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(GOLD_PRICES_FILE, "w") as f:
                json.dump(prices, f, indent=2)
            return {"status": "success", "message": f"تم تحديث سعر الذهب في {gp.city}"}
    
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

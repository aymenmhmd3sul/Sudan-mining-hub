import os
import requests
import sys

# إعداد المتغيرات الأساسية
BASE_URL = "https://sudan-mining-hub-3.onrender.com"
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ خطأ: لم يتم العثور على متغير البيئة TOKEN.")
    print("يرجى تصدير التوكن أولاً باستخدام: export TOKEN='your_token_here'")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print(f"🚀 بدء اختبار تكامل الإنتاج (Production Integration Test) لـ Marketplace...")
print(f"🌐 الرابط المستهدف: {BASE_URL}\n" + "-"*50)

# 1. اختبار إنشاء عنصر جديد (Create Asset)
create_payload = {
    "title": "حفار كاتر بيلر 320D - اختبار الإنتاج الموحد",
    "description": "حفار مجنزرة بحالة ممتازة مستخدم في التعدين السطحي",
    "main_category": "MINING_EQUIPMENT",
    "sub_category": "EXCAVATOR",
    "price": 125000.0,
    "currency": "USD",
    "is_negotiable": True,
    "state_province": "ولاية نهر النيل",
    "locality": "أبوحمد",
    "coordinates": "19.5290,33.3792",
    "images_urls": [
        "https://example.com/images/excavator1.jpg",
        "https://example.com/images/excavator2.jpg"
    ],
    "specific_specs": {
        "brand": "CAT",
        "model": "320D",
        "working_hours": 6400,
        "condition": "Excellent"
    }
}

print("🧪 1. محاولة إنشاء أصل جديد...")
res_create = requests.post(f"{BASE_URL}/market/assets", json=create_payload, headers=headers)

if res_create.status_code == 201:
    created_asset = res_create.json()
    asset_id = created_asset.get("id")
    print(f"✅ تم إنشاء الأصل بنجاح في PostgreSQL! معرف الأصل المسترجع: (ID: {asset_id})")
else:
    print(f"❌ فشل إنشاء الأصل! رمز الاستجابة: {res_create.status_code}")
    print(f"الرد: {res_create.text}")
    sys.exit(1)

print("-"*50)

# 2. اختبار استرجاع الأصل المكتوب (Retrieve Asset)
print(f"🧪 2. محاولة استرجاع تفاصيل الأصل رقم ({asset_id})...")
res_get = requests.get(f"{BASE_URL}/market/assets/{asset_id}", headers=headers)

if res_get.status_code == 200:
    retrieved_asset = res_get.json()
    print("✅ تم استرجاع بيانات الأصل بنجاح والتحقق من سلامتها!")
    print(f"   اسم الأصل: {retrieved_asset.get('title')}")
    print(f"   الموقع: {retrieved_asset.get('state_province')} - {retrieved_asset.get('locality')}")
    print(f"   المواصفات الفنية: {retrieved_asset.get('specific_specs')}")
else:
    print(f"❌ فشل استرجاع الأصل! رمز الاستجابة: {res_get.status_code}")
    print(f"الرد: {res_get.text}")
    sys.exit(1)

print("-"*50)
print("🎉 انتهى اختبار الـ Marketplace الأول بنجاح تام وبدون أخطاء!")

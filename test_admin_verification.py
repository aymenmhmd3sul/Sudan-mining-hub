import requests
import json

BASE_URL = "https://sudan-mining-hub-3.onrender.com"

print("🔍 فحص تسجيل دخول حساب مدير النظام (Admin Verification)...\n")

# بيانات حساب المشرف الفعلي
admin_credentials = {
    "username": "aymen.mhmd3@gmail.com",
    "password": "SudanMining@2026"
}

# 1. اختبار نقطة نهاية تسجيل الدخول والحصول على التوكن
print("🧪 اختبار طلب المصادقة عبر /auth/login...")
try:
    login_resp = requests.post(f"{BASE_URL}/auth/login", data=admin_credentials)
    print(f"📥 استجابة السيرفر: [{login_resp.status_code}]")
    
    if login_resp.status_code == 200:
        token_data = login_resp.json()
        access_token = token_data.get("access_token")
        print("✅ تم الحصول على Access Token بنجاح!")
        
        # 2. اختبار استرجاع بيانات الملف الشخصي من الـ ORM الموحد عبر التوكن
        print("\n🧪 اختبار جلب كائن المستخدم من الـ ORM عبر /api/users/profile...")
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_resp = requests.get(f"{BASE_URL}/api/users/profile", headers=headers)
        
        print(f"📥 استجابة السيرفر: [{profile_resp.status_code}]")
        print(json.dumps(profile_resp.json(), indent=4, ensure_ascii=False))
    else:
        print("❌ فشل تسجيل الدخول، تحقق من استجابة السيرفر:")
        print(json.dumps(login_resp.json(), indent=4, ensure_ascii=False))
        
except Exception as e:
    print(f"❌ حدث خطأ غير متوقع أثناء الفحص: {e}")

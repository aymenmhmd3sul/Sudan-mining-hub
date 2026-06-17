from fastapi import FastAPI, HTMLResponse, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
from datetime import datetime
import json
import os

app = FastAPI()

# إعداد القوالب (إن وجدت) أو استخدام HTML مباشر
# templates = Jinja2Templates(directory="templates")

async def get_gold_price():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://api.gold-api.com/price/XAU")
            if response.status_code == 200:
                data = response.json()
                return data.get("price", 4315.09)
            return 4315.09
    except:
        return 4315.09

# ========== الصفحات العامة ==========

@app.get("/", response_class=HTMLResponse)
async def root():
    gold = await get_gold_price()
    now = datetime.now().strftime("%I:%M %p")
    return f'''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة السودان للتعدين</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Tahoma',Arial,sans-serif; background:#0f172a; color:#f1f5f9; min-height:100vh; padding:20px; }}
        .container {{ max-width:1300px; margin:0 auto; }}
        .header {{ display:flex; justify-content:space-between; align-items:center; padding:20px 0; border-bottom:1px solid rgba(255,255,255,0.05); margin-bottom:30px; flex-wrap:wrap; gap:15px; }}
        .header h1 {{ font-size:2rem; font-weight:700; background:linear-gradient(135deg,#fbbf24,#f59e0b); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
        .gold-price {{ background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.2); padding:12px 24px; border-radius:12px; font-size:1.3rem; font-weight:600; color:#fbbf24; }}
        .gold-price span {{ font-size:0.8rem; color:#94a3b8; font-weight:400; }}
        .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:20px; margin-bottom:30px; }}
        .card {{ background:linear-gradient(145deg,#1e293b,#0f172a); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:24px 20px; text-align:center; transition:transform 0.3s; box-shadow:0 4px 15px rgba(0,0,0,0.2); cursor:pointer; }}
        .card:hover {{ transform:translateY(-6px); box-shadow:0 12px 30px rgba(0,0,0,0.4); }}
        .card-icon {{ font-size:2.5rem; margin-bottom:8px; display:block; }}
        .card-number {{ font-size:2rem; font-weight:700; color:#fbbf24; margin:6px 0; }}
        .card-number.green {{ color:#22c55e; }}
        .card-number.blue {{ color:#3b82f6; }}
        .card-number.purple {{ color:#a855f7; }}
        .card-number.pink {{ color:#ec4899; }}
        .card-label {{ color:#94a3b8; font-size:0.9rem; }}
        .card-sub {{ color:#64748b; font-size:0.75rem; margin-top:4px; }}
        .flex {{ display:flex; gap:12px; flex-wrap:wrap; justify-content:center; margin-top:10px; }}
        .btn {{ padding:10px 24px; background:#22c55e; border:none; color:white; border-radius:10px; font-size:0.95rem; font-weight:600; cursor:pointer; transition:0.2s; font-family:inherit; text-decoration:none; display:inline-block; }}
        .btn:hover {{ transform:scale(1.05); box-shadow:0 8px 25px rgba(34,197,94,0.3); }}
        .btn-blue {{ background:#3b82f6; }}
        .btn-blue:hover {{ box-shadow:0 8px 25px rgba(59,130,246,0.3); }}
        .status-badge {{ display:inline-block; padding:4px 14px; background:#22c55e; color:#fff; border-radius:20px; font-size:0.75rem; font-weight:600; margin-right:8px; }}
        .footer {{ margin-top:40px; padding-top:20px; border-top:1px solid rgba(255,255,255,0.05); text-align:center; color:#64748b; font-size:0.9rem; }}
        .section-title {{ font-size:1.3rem; font-weight:600; margin-bottom:15px; color:#e2e8f0; }}
        .content-box {{ background:#1e293b; padding:20px; border-radius:12px; margin-top:20px; border:1px solid rgba(255,255,255,0.05); }}
        @media (max-width:600px) {{ .header h1 {{ font-size:1.4rem; }} .gold-price {{ font-size:1rem; padding:8px 16px; }} .grid {{ grid-template-columns:repeat(2,1fr); }} .card-number {{ font-size:1.4rem; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⛏️ منصة السودان للتعدين</h1>
            <div class="gold-price">💰 USD {gold} <span>| PAXG</span></div>
        </div>
        <div class="grid">
            <div class="card" onclick="location.href='/buyer'">
                <span class="card-icon">🛒</span>
                <div class="card-number blue">واجهة المشتري</div>
                <div class="card-label">تقديم طلب شراء</div>
                <div class="card-sub">اطلب الذهب الآن</div>
            </div>
            <div class="card" onclick="location.href='/seller'">
                <span class="card-icon">🏪</span>
                <div class="card-number purple">واجهة التاجر</div>
                <div class="card-label">إدارة الطلبات</div>
                <div class="card-sub">استجب لطلبات المشترين</div>
            </div>
            <div class="card" onclick="location.href='/admin'">
                <span class="card-icon">⚙️</span>
                <div class="card-number pink">لوحة المشرف</div>
                <div class="card-label">إدارة النظام</div>
                <div class="card-sub">المستخدمين، الإعلانات، الأسعار</div>
            </div>
        </div>
        <div class="section-title">🚀 التنقل السريع</div>
        <div class="flex">
            <a href="/buyer" class="btn btn-blue">المشتري</a>
            <a href="/seller" class="btn btn-blue">التاجر</a>
            <a href="/admin" class="btn btn-blue">المشرف</a>
            <a href="/dashboard" class="btn">لوحة التحكم</a>
        </div>
        <div style="margin-top:30px; padding:20px; background:#1e293b; border-radius:12px; border:1px solid rgba(255,255,255,0.05);">
            🟢 النظام مباشر <span class="status-badge">Live</span> — آخر تحديث: {now}
        </div>
        <div class="footer">
            منصة السودان للتعدين © 2026 — جميع الحقوق محفوظة
        </div>
    </div>
</body>
</html>
'''

# ========== صفحات المشتري ==========

@app.get("/buyer", response_class=HTMLResponse)
async def buyer_dashboard():
    gold = await get_gold_price()
    return f'''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>المشتري - منصة السودان للتعدين</title>
<style>
body {{ background:#0f172a; color:white; font-family:Tahoma; padding:20px; }}
.container {{ max-width:800px; margin:auto; }}
.box {{ background:#1e293b; padding:20px; margin:10px 0; border-radius:12px; }}
.btn {{ padding:10px 20px; background:#22c55e; border:none; color:white; border-radius:8px; cursor:pointer; }}
</style>
</head>
<body>
<div class="container">
    <h1>🛒 واجهة المشتري</h1>
    <div class="box">
        <h3>تقديم طلب شراء</h3>
        <form action="/api/orders/create" method="post">
            <input type="text" name="item" placeholder="الذهب (جرام)" required><br><br>
            <input type="number" name="quantity" placeholder="الكمية" required><br><br>
            <input type="text" name="price" placeholder="السعر المطلوب" value="{gold}"><br><br>
            <button class="btn" type="submit">إرسال الطلب</button>
        </form>
    </div>
    <div class="box">
        <h3>طلباتي الحالية</h3>
        <p>سيتم عرض طلباتك هنا بعد الإرسال.</p>
    </div>
    <a href="/">⬅️ العودة للرئيسية</a>
</div>
</body>
</html>
'''

# ========== صفحات التاجر ==========

@app.get("/seller", response_class=HTMLResponse)
async def seller_dashboard():
    return f'''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>التاجر - منصة السودان للتعدين</title>
<style>
body {{ background:#0f172a; color:white; font-family:Tahoma; padding:20px; }}
.container {{ max-width:800px; margin:auto; }}
.box {{ background:#1e293b; padding:20px; margin:10px 0; border-radius:12px; }}
.btn {{ padding:10px 20px; background:#22c55e; border:none; color:white; border-radius:8px; cursor:pointer; }}
</style>
</head>
<body>
<div class="container">
    <h1>🏪 واجهة التاجر</h1>
    <div class="box">
        <h3>طلبات المشترين</h3>
        <p>هنا تظهر طلبات الشراء الواردة.</p>
        <ul>
            <li>طلب #1: 5 جرام بسعر 4320$ <button class="btn" onclick="alert('تم قبول الطلب')">قبول</button> <button class="btn" style="background:#dc2626;">رفض</button></li>
            <li>طلب #2: 10 جرام بسعر 4300$ <button class="btn" onclick="alert('تم قبول الطلب')">قبول</button> <button class="btn" style="background:#dc2626;">رفض</button></li>
        </ul>
    </div>
    <a href="/">⬅️ العودة للرئيسية</a>
</div>
</body>
</html>
'''

# ========== لوحة المشرف (admin) ==========

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():
    return f'''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>المشرف - منصة السودان للتعدين</title>
<style>
body {{ background:#0f172a; color:white; font-family:Tahoma; padding:20px; }}
.container {{ max-width:1000px; margin:auto; }}
.box {{ background:#1e293b; padding:20px; margin:10px 0; border-radius:12px; }}
.btn {{ padding:10px 20px; background:#22c55e; border:none; color:white; border-radius:8px; cursor:pointer; }}
</style>
</head>
<body>
<div class="container">
    <h1>⚙️ لوحة المشرف</h1>
    <div class="box">
        <h3>إدارة المستخدمين</h3>
        <p>قائمة المستخدمين (نموذج):</p>
        <ul>
            <li>مشتري تجريبي (buyer@test.com) - دور: مشتري</li>
            <li>تاجر تجريبي (seller@test.com) - دور: تاجر</li>
        </ul>
    </div>
    <div class="box">
        <h3>إضافة إعلان جديد</h3>
        <form>
            <input type="text" placeholder="العنوان (عربي)"><br><br>
            <input type="text" placeholder="العنوان (إنجليزي)"><br><br>
            <textarea placeholder="الوصف"></textarea><br><br>
            <button class="btn" type="submit">نشر الإعلان</button>
        </form>
    </div>
    <a href="/">⬅️ العودة للرئيسية</a>
</div>
</body>
</html>
'''

# ========== واجهات برمجة التطبيقات (API) الحالية ==========

@app.get("/api/price")
async def get_price():
    return {"gold": await get_gold_price()}

@app.get("/api/gold")
async def get_gold():
    return {"gold": await get_gold_price()}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/dashboard")
async def dashboard():
    gold = await get_gold_price()
    return f'''
<!DOCTYPE html>
<html>
<head><title>منصة السودان للتعدين</title></head>
<body style="background:#0f172a;color:white;font-family:Arial;padding:20px;">
<h1>⛏️ منصة السودان للتعدين</h1>
<p>سعر الذهب: {gold} USD</p>
<p>✅ النظام يعمل</p>
</body>
</html>
'''

# مسارات API إضافية للطلبات (نموذجية)
@app.post("/api/orders/create")
async def create_order(request: Request):
    # هنا سنضيف منطق حفظ الطلب في قاعدة البيانات
    return {"message": "تم إنشاء الطلب بنجاح"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

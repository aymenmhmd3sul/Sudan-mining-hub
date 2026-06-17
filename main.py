from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
from datetime import datetime

app = FastAPI()

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
        .btn {{ padding:10px 24px; background:#22c55e; border:none; color:white; border-radius:10px; font-size:0.95rem; font-weight:600; cursor:pointer; transition:0.2s; font-family:inherit; }}
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
            <div class="card" onclick="showSection('gold')">
                <span class="card-icon">📊</span>
                <div class="card-number green">{gold}</div>
                <div class="card-label">سعر الأونصة</div>
                <div class="card-sub">تحديث مباشر</div>
            </div>
            <div class="card" onclick="showSection('traders')">
                <span class="card-icon">🏦</span>
                <div class="card-number blue">٢٤</div>
                <div class="card-label">التجار النشطون</div>
                <div class="card-sub">قائمة معتمدة</div>
            </div>
            <div class="card" onclick="showSection('orders')">
                <span class="card-icon">📦</span>
                <div class="card-number purple">١٤٢</div>
                <div class="card-label">الطلبات المفتوحة</div>
                <div class="card-sub">اليوم</div>
            </div>
            <div class="card" onclick="showSection('ads')">
                <span class="card-icon">⚡</span>
                <div class="card-number pink">٨</div>
                <div class="card-label">إعلانات جديدة</div>
                <div class="card-sub">آخر ساعة</div>
            </div>
        </div>
        <div class="section-title">🚀 التنقل السريع</div>
        <div class="flex">
            <button class="btn" onclick="showSection('traders')">التجار</button>
            <button class="btn btn-blue" onclick="showSection('orders')">الطلبات</button>
            <button class="btn btn-blue" onclick="showSection('ads')">الإعلانات</button>
            <button class="btn btn-blue" onclick="showSection('mining')">التعدين</button>
            <button class="btn btn-blue" onclick="showSection('subscribe')">الاشتراك</button>
        </div>
        <div id="content" class="content-box" style="display:none;">
            <h2 id="content-title"></h2>
            <p id="content-text"></p>
        </div>
        <div style="margin-top:30px; padding:20px; background:#1e293b; border-radius:12px; border:1px solid rgba(255,255,255,0.05);">
            🟢 النظام مباشر <span class="status-badge">Live</span> — آخر تحديث: {now}
        </div>
        <div class="footer">
            منصة السودان للتعدين © 2026 — جميع الحقوق محفوظة
        </div>
    </div>
    <script>
        const sections = {{
            'traders': {{ 'title':'👥 التجار', 'text':'قائمة التجار المعتمدين في منصة السودان للتعدين. يمكنك عرض ملفاتهم والتواصل معهم.' }},
            'orders': {{ 'title':'📦 الطلبات', 'text':'جميع طلبات الشراء والبيع المفتوحة. يمكنك تصفيتها حسب النوع أو التاريخ.' }},
            'ads': {{ 'title':'📢 الإعلانات', 'text':'إعلانات التعدين والذهب المضافة حديثاً. تواصل مع المعلنين مباشرة.' }},
            'mining': {{ 'title':'⛏️ التعدين', 'text':'معلومات عن نشاط التعدين في السودان، أحدث المشاريع والفرص المتاحة.' }},
            'subscribe': {{ 'title':'📝 الاشتراك', 'text':'اشترك الآن في منصة السودان للتعدين واحصل على مميزات حصرية.' }},
            'gold': {{ 'title':'📊 سعر الذهب', 'text':'سعر الأونصة الذهب محدث مباشرة من الأسواق العالمية.' }}
        }};
        function showSection(section) {{
            const content = document.getElementById('content');
            const title = document.getElementById('content-title');
            const text = document.getElementById('content-text');
            if (sections[section]) {{
                title.textContent = sections[section].title;
                text.textContent = sections[section].text;
                content.style.display = 'block';
            }}
        }}
    </script>
</body>
</html>
'''

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
<head><title>Sudan Mining Hub</title>
<meta charset="utf-8">
<style>
body {{ background:#0f172a; color:white; font-family:Arial; padding:20px; }}
.box {{ background:#1e293b; padding:20px; margin:10px 0; border-radius:12px; }}
button {{ padding:10px; background:#22c55e; border:none; color:white; border-radius:8px; cursor:pointer; }}
button:hover {{ background:#16a34a; }}
</style>
</head>
<body>
<h1>🟡 Sudan Mining Hub</h1>
<div class="box"><h3>Gold Price</h3><p style="font-size:24px">{gold} USD</p></div>
<div class="box"><h3>Status</h3><p>✅ Running</p></div>
<div class="box"><button onclick="alert('✅ زر يعمل بشكل صحيح!')">Test Button</button></div>
</body>
</html>
'''

@app.get("/traders")
async def traders():
    return {"page": "التجار", "message": "قائمة التجار"}

@app.get("/orders")
async def orders():
    return {"page": "الطلبات", "message": "قائمة الطلبات"}

@app.get("/ads")
async def ads():
    return {"page": "الإعلانات", "message": "قائمة الإعلانات"}

@app.get("/mining")
async def mining():
    return {"page": "التعدين", "message": "معلومات التعدين"}

@app.get("/subscribe")
async def subscribe():
    return {"page": "الاشتراك", "message": "صفحة الاشتراك"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

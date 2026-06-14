from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

def price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=5)
        return round(float(r.json()["price"]),2)
    except:
        return 2330.0

@app.get("/")
def root():
    return {"status":"ok"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/policy", response_class=HTMLResponse)
def policy():
    return HTMLResponse("""
    <html><body style="background:#0f172a;color:white;font-family:Arial;padding:20px">
    <h1>سياسة المنصة</h1>
    <p>منصة عرض أسعار الذهب فقط.</p>
    </body></html>
    """)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    gold = price()

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sudan Mining Hub</title>

<style>
body {{margin:0;font-family:Arial;background:#0f172a;color:white}}
.header {{background:#111827;padding:18px;text-align:center;font-size:26px;font-weight:bold}}
.ticker {{background:#1e293b;padding:10px;text-align:center}}
.grid {{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;padding:15px}}
.card {{background:#1f2937;padding:18px;border-radius:12px;text-align:center;cursor:pointer}}
.card:hover {{background:#374151}}
.panel {{margin:15px;padding:20px;background:#111827;border-radius:12px;min-height:120px}}
.footer {{text-align:center;padding:15px;background:#111827}}
a {{color:#38bdf8}}
</style>

<script>
function showSection(title,content){{
document.getElementById("panel").innerHTML =
"<h2>"+title+"</h2><p>"+content+"</p>";
}}
</script>

</head>

<body>

<div class="header">🟡 Sudan Mining Hub</div>

<div class="ticker">
🟡 أونصة الذهب: {gold} USD | 🔄 مباشر
</div>

<div class="grid">

<div class="card" onclick="showSection(الطلبات,لا
توجد
طلبات
حالياً)">📦 الطلبات</div>
<div class="card" onclick="showSection(التجار,لا
يوجد
تجار
حالياً)">👤 التجار</div>
<div class="card" onclick="showSection(التعدين,معدات
التعدين
والخدمات)">⛏️ التعدين</div>
<div class="card" onclick="showSection(الإعلانات,لا
توجد
إعلانات)">📢 الإعلانات</div>
<div class="card" onclick="showSection(الاشتراك,خطط
الاشتراك
قريباً)">💳 الاشتراك</div>

</div>

<div id="panel" class="panel">
اضغط على أي قسم لعرض التفاصيل
</div>

<div class="footer">
<a href="/policy">سياسة المنصة</a>
</div>

</body>
</html>
""")


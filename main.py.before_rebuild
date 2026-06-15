from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

def get_price():
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
    <html dir="rtl">
    <body style="background:#0f172a;color:white;font-family:Arial;padding:20px">
        <h1>سياسة المنصة</h1>
        <p>منصة عرض أسعار الذهب والمعلومات السوقية.</p>
    </body>
    </html>
    """)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    gold = get_price()

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sudan Mining Hub</title>

<style>
body {{
margin:0;
font-family:Arial;
background:#0b1220;
color:white;
-webkit-user-select:none;
user-select:none;
touch-action:manipulation;
}}

.topbar {{
position:sticky;
top:0;
background:#0f172a;
padding:14px;
text-align:center;
font-size:20px;
font-weight:bold;
border-bottom:1px solid #1f2937;
}}

.pricebar {{
display:flex;
justify-content:space-around;
padding:10px;
background:#111827;
font-size:14px;
color:#cbd5e1;
}}

.grid {{
display:grid;
grid-template-columns:1fr 1fr;
gap:10px;
padding:12px;
}}

.card {{
background:#1f2937;
padding:18px;
border-radius:14px;
text-align:center;
font-size:15px;
cursor:pointer;
transition:0.15s;
}}

.card:active {{
transform:scale(0.95);
background:#374151;
}}

.panel {{
margin:12px;
padding:18px;
background:#111827;
border-radius:12px;
min-height:140px;
}}

.footer {{
text-align:center;
padding:15px;
background:#0f172a;
border-top:1px solid #1f2937;
}}

a {{
color:#38bdf8;
text-decoration:none;
}}

.lang {{
position:fixed;
top:10px;
left:10px;
background:#1f2937;
padding:6px 10px;
border-radius:8px;
font-size:12px;
cursor:pointer;
}}

</style>

<script>

let lang = "ar";

function toggleLang() {{
lang = (lang === "ar") ? "en" : "ar";

document.getElementById("title").innerText =
lang==="ar" ? "🟡 منصة السودان للتعدين" : "🟡 Sudan Mining Hub";

document.getElementById("p1").innerText = lang==="ar" ? "📦 الطلبات" : "Orders";
document.getElementById("p2").innerText = lang==="ar" ? "👤 التجار" : "Traders";
document.getElementById("p3").innerText = lang==="ar" ? "⛏️ التعدين" : "Mining";
document.getElementById("p4").innerText = lang==="ar" ? "📢 الإعلانات" : "Ads";
document.getElementById("p5").innerText = lang==="ar" ? "💳 الاشتراك" : "Subscription";
}}

function openTab(title, text) {{
document.getElementById("panel").innerHTML =
"<h2>"+title+"</h2><p>"+text+"</p>";
}}

</script>

</head>

<body>

<div class="lang" onclick="toggleLang()">AR/EN</div>

<div class="topbar" id="title">🟡 منصة السودان للتعدين</div>

<div class="pricebar">
<div>🟡 أونصة: {gold} USD</div>
<div>🔄 Live</div>
</div>

<div class="grid">

<div class="card" id="p1" onclick="openTab(الطلبات,لا
توجد
طلبات
حالياً)">📦 الطلبات</div>
<div class="card" id="p2" onclick="openTab(التجار,لا
يوجد
تجار
حالياً)">👤 التجار</div>
<div class="card" id="p3" onclick="openTab(التعدين,معدات
التعدين
والخدمات)">⛏️ التعدين</div>
<div class="card" id="p4" onclick="openTab(الإعلانات,لا
توجد
إعلانات)">📢 الإعلانات</div>
<div class="card" id="p5" onclick="openTab(الاشتراك,خطط
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


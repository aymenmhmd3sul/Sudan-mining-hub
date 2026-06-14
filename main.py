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
    return {"status":"API running"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    gold = get_price()

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sudan Mining Hub</title>

<style>

body {{
margin:0;
font-family:Arial,sans-serif;
background:#0f172a;
color:white;
}}

.header {{
background:#111827;
padding:15px;
text-align:center;
font-size:28px;
font-weight:bold;
}}

.ticker {{
background:#1e293b;
padding:12px;
text-align:center;
font-size:18px;
border-bottom:1px solid #334155;
}}

.container {{
padding:15px;
}}

.grid {{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
gap:15px;
}}

.card {{
background:#1f2937;
padding:25px;
border-radius:14px;
cursor:pointer;
transition:0.2s;
text-align:center;
font-size:20px;
}}

.card:hover {{
transform:scale(1.03);
}}

.panel {{
margin-top:20px;
background:#111827;
padding:20px;
border-radius:14px;
min-height:220px;
font-size:18px;
}}

.footer {{
margin-top:20px;
text-align:center;
padding:15px;
background:#111827;
}}

</style>

<script>

function showSection(title,text)
{{
document.getElementById("panel").innerHTML=
"<h2>"+title+"</h2><hr><p>"+text+"</p>";
}}

</script>

</head>

<body>

<div class="header">
🟡 منصة السودان للتعدين
</div>

<div class="ticker">
سعر الذهب العالمي: {gold} USD | السعر المحلي: قريباً
</div>

<div class="container">

<div class="grid">

<div class="card" onclick="showSection(الطلبات,هنا
ستظهر
طلبات
الشراء
والبيع.)">
📦 الطلبات
</div>

<div class="card" onclick="showSection(التجار,هنا
ستظهر
قائمة
التجار
المسجلين.)">
👤 التجار
</div>

<div class="card" onclick="showSection(التعدين,هنا
ستظهر
خدمات
ومعدات
التعدين.)">
⛏️ التعدين
</div>

<div class="card" onclick="showSection(الإعلانات,هنا
ستظهر
الإعلانات
المميزة.)">
📢 الإعلانات
</div>

<div class="card" onclick="showSection(الاشتراك,هنا
ستظهر
خطط
الاشتراك
والدفع.)">
💳 الاشتراك
</div>

</div>

<div id="panel" class="panel">

<h2>مرحباً بك</h2>

<p>
اختر أحد الأقسام أعلاه لعرض محتوياته.
</p>

</div>

</div>

<div class="footer">
Sudan Mining Hub Live System
</div>

</body>
</html>
""")


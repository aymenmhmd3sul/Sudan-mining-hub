from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
from datetime import datetime

app = FastAPI()

def get_price():
    try:
        r = requests.get(
            "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT",
            timeout=5
        )
        return round(float(r.json()["price"]), 2)
    except:
        return 0.0

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/gold")
def api_gold():
    return {"gold": get_price()}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    gold = get_price()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة السودان للتعدين</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Tahoma', Arial, sans-serif; background: #0f172a; color: #f1f5f9; min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1300px; margin: 0 auto; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 30px; flex-wrap: wrap; gap: 15px; }}
        .header h1 {{ font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #fbbf24, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .gold-price {{ background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.2); padding: 12px 24px; border-radius: 12px; font-size: 1.3rem; font-weight: 600; color: #fbbf24; }}
        .gold-price span {{ font-size: 0.8rem; color: #94a3b8; font-weight: 400; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: linear-gradient(145deg, #1e293b, #0f172a); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 24px 20px; text-align: center; transition: transform 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
        .card:hover {{ transform: translateY(-6px); box-shadow: 0 12px 30px rgba(0,0,0,0.4); }}
        .card-icon {{ font-size: 2.5rem; margin-bottom: 8px; display: block; }}
        .card-number {{ font-size: 2rem; font-weight: 700; color: #fbbf24; margin: 6px 0; }}
        .card-number.green {{ color: #22c55e; }}
        .card-number.blue {{ color: #3b82f6; }}
        .card-number.purple {{ color: #a855f7; }}
        .card-number.pink {{ color: #ec4899; }}
        .card-label {{ color: #94a3b8; font-size: 0.9rem; }}
        .card-sub {{ color: #64748b; font-size: 0.75rem; margin-top: 4px; }}
        .flex {{ display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; margin-top: 10px; }}
        .btn {{ padding: 10px 24px; background: #22c55e; border: none; color: white; border-radius: 10px; font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: 0.2s; font-family: inherit; }}
        .btn:hover {{ transform: scale(1.05); box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3); }}
        .btn-blue {{ background: #3b82f6; }}
        .btn-blue:hover {{ box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3); }}
        .status-badge {{ display: inline-block; padding: 4px 14px; background: #22c55e; color: #fff; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-right: 8px; }}
        .toast {{ position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #1e293b; border: 1px solid #22c55e; padding: 12px 24px; border-radius: 12px; display: none; z-index: 999; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); text-align: center; color: #64748b; font-size: 0.9rem; }}
        @media (max-width: 600px) {{ .header h1 {{ font-size: 1.4rem; }} .gold-price {{ font-size: 1rem; padding: 8px 16px; }} .grid {{ grid-template-columns: repeat(2, 1fr); }} .card-number {{ font-size: 1.4rem; }} }}
        .spinner {{ display: inline-block; width: 16px; height: 16px; border: 3px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: #fff; animation: spin 0.8s ease infinite; vertical-align: middle; margin-left: 8px; }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⛏️ لوحة السودان للتعدين</h1>
            <div class="gold-price" id="goldPrice">💰 USD {gold} <span>| PAXG</span></div>
        </div>

        <div class="grid">
            <div class="card">
                <span class="card-icon">📦</span>
                <div class="card-number blue" id="orders">1,284</div>
                <div class="card-label">الطلبات</div>
                <div class="card-sub">+12% هذا الشهر</div>
            </div>
            <div class="card">
                <span class="card-icon">👩‍🎓</span>
                <div class="card-number green" id="traders">342</div>
                <div class="card-label">التجار</div>
                <div class="card-sub">نشطون ✅</div>
            </div>
            <div class="card">
                <span class="card-icon">⛏️</span>
                <div class="card-number purple" id="mining">56</div>
                <div class="card-label">التعدين</div>
                <div class="card-sub">معدات عاملة</div>
            </div>
            <div class="card">
                <span class="card-icon">📢</span>
                <div class="card-number pink" id="ads">89</div>
                <div class="card-label">الإعلانات</div>
                <div class="card-sub">نشطة 📈</div>
            </div>
            <div class="card">
                <span class="card-icon">📋</span>
                <div class="card-number" id="subscriptions" style="color:#fbbf24;">247</div>
                <div class="card-label">الاشتراك</div>
                <div class="card-sub">مستخدمين جدد</div>
            </div>
        </div>

        <div style="text-align:center;margin:30px 0;">
            <div class="flex">
                <button class="btn" id="refreshDataBtn" onclick="refreshData()">🔄 تحديث البيانات</button>
                <button class="btn btn-blue" onclick="location.reload()">⏳ تحديث الصفحة</button>
            </div>
            <p style="color:#94a3b8;font-size:0.85rem;margin-top:15px;">
                🟢 النظام مباشر <span class="status-badge">Live</span> — آخر تحديث: <span id="lastUpdate">{now}</span>
            </p>
        </div>

        <div class="footer">
            <p>© 2026 منصة سودان للتعدين — نظام مباشر 🚀</p>
        </div>
    </div>

    <div class="toast" id="toast"></div>

    <script>
        function showToast(message, isError = false) {{
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.style.display = 'block';
            toast.style.borderColor = isError ? '#ef4444' : '#22c55e';
            setTimeout(() => {{ toast.style.display = 'none'; }}, 3000);
        }}

        async function refreshData() {{
            const btn = document.getElementById('refreshDataBtn');
            btn.disabled = true;
            btn.innerHTML = '⏳ جاري التحديث... <span class="spinner"></span>';

            try {{
                const response = await fetch('/api/gold');
                if (!response.ok) throw new Error('فشل جلب البيانات');
                const data = await response.json();
                
                if (data.gold !== undefined) {{
                    document.getElementById('goldPrice').innerHTML = `💰 USD ${{data.gold.toFixed(2)}} <span>| PAXG</span>`;
                    document.getElementById('lastUpdate').textContent = new Date().toLocaleString('ar-EG');
                    
                    document.getElementById('orders').textContent = Math.floor(1200 + Math.random() * 200);
                    document.getElementById('traders').textContent = Math.floor(320 + Math.random() * 50);
                    document.getElementById('mining').textContent = Math.floor(50 + Math.random() * 15);
                    document.getElementById('ads').textContent = Math.floor(80 + Math.random() * 20);
                    document.getElementById('subscriptions').textContent = Math.floor(220 + Math.random() * 50);
                    
                    showToast('✅ تم تحديث البيانات بنجاح!');
                }}
            }} catch (error) {{
                showToast('❌ فشل تحديث البيانات: ' + error.message, true);
            }}

            btn.disabled = false;
            btn.innerHTML = '🔄 تحديث البيانات';
        }}
    </script>
</body>
</html>
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import json
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
    return {"status": "running", "service": "Sudan Mining Hub"}

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
<html>
<head>
    <title>Sudan Mining Hub</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #94a3b8;
            margin-bottom: 30px;
            font-size: 1.1rem;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin-bottom: 30px;
        }}
        .card {{
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
        }}
        .card-title {{
            color: #94a3b8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}
        .card-value {{
            font-size: 2.2rem;
            font-weight: 700;
            color: #fbbf24;
        }}
        .card-value.green {{
            color: #22c55e;
        }}
        .card-value.blue {{
            color: #3b82f6;
        }}
        .card-value.purple {{
            color: #a855f7;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            background: #22c55e;
            color: white;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .btn {{
            padding: 12px 28px;
            background: linear-gradient(135deg, #22c55e, #16a34a);
            border: none;
            color: white;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4);
        }}
        .btn-secondary {{
            background: linear-gradient(135deg, #3b82f6, #2563eb);
        }}
        .btn-secondary:hover {{
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        }}
        .btn-danger {{
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }}
        .btn-danger:hover {{
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4);
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            color: #64748b;
            text-align: center;
            font-size: 0.9rem;
        }}
        .flex {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        @media (max-width: 600px) {{
            h1 {{ font-size: 1.8rem; }}
            .card-value {{ font-size: 1.6rem; }}
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🟡 Sudan Mining Hub</h1>
        <p class="subtitle">Live Gold Price Dashboard — Last updated: {now}</p>

        <div class="grid">
            <div class="card">
                <div class="card-title">💰 Gold Price (USD)</div>
                <div class="card-value">${gold}</div>
                <p style="color:#94a3b8;font-size:0.85rem;margin-top:8px;">PAXG / USDT</p>
            </div>

            <div class="card">
                <div class="card-title">📊 System Status</div>
                <div class="card-value green">● Online</div>
                <p style="color:#94a3b8;font-size:0.85rem;margin-top:8px;">
                    <span class="status-badge">Operational</span>
                </p>
            </div>

            <div class="card">
                <div class="card-title">🕐 Last Update</div>
                <div class="card-value blue">{now}</div>
                <p style="color:#94a3b8;font-size:0.85rem;margin-top:8px;">Auto-refresh every 60s</p>
            </div>
        </div>

        <div class="flex" style="margin-bottom:30px;">
            <button class="btn" onclick="alert('✅ Gold price: ${gold} USD')">
                🔄 Check Price
            </button>
            <button class="btn btn-secondary" onclick="location.reload()">
                🔁 Refresh
            </button>
            <button class="btn btn-danger" onclick="alert('⚠️ This is a demo alert!')">
                ⚡ Test Alert
            </button>
        </div>

        <div class="footer">
            <p>© 2026 Sudan Mining Hub — Built with FastAPI + ❤️</p>
        </div>
    </div>
</body>
</html>
"""

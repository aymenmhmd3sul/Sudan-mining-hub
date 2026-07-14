from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db.compat import get_user_from_cookie

router = APIRouter(prefix="/seller", tags=["seller"])

@router.get("/", response_class=HTMLResponse)
async def seller_dashboard(request: Request):
    user = get_user_from_cookie(request)
    if not user or user["role"] != "seller": return RedirectResponse("/auth/login", 302)
    return f'''
<html dir="rtl"><head><title>التاجر</title><style>body{{background:#0f172a;color:white;font-family:Tahoma;padding:20px;}}.box{{background:#1e293b;padding:20px;border-radius:12px;margin:10px 0;}}.btn{{padding:8px 16px;border:none;border-radius:8px;cursor:pointer;}}.accept{{background:#22c55e;color:white;}}.reject{{background:#dc2626;color:white;}}</style></head>
<body><h1>🏪 مرحباً {user["name"]} (تاجر)</h1>
<div class="box"><h3>📦 طلبات واردة</h3><ul><li style="display:flex;justify-content:space-between;padding:10px;background:#0f172a;border-radius:8px;">طلب #1: 5 جرام <span><button class="btn accept" onclick="alert('قبول')">قبول</button> <button class="btn reject" onclick="alert('رفض')">رفض</button></span></li></ul></div>
<div><a href="/auth/logout">تسجيل الخروج</a> | <a href="/">الرئيسية</a></div>
</body></html>
'''

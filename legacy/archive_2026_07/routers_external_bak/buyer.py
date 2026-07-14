from fastapi import APIRouter, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db.compat import get_user_from_cookie, get_gold_price

router = APIRouter(prefix="/buyer", tags=["buyer"])

@router.get("/", response_class=HTMLResponse)
async def buyer_dashboard(request: Request):
    user = get_user_from_cookie(request)
    if not user or user["role"] != "buyer": return RedirectResponse("/auth/login", 302)
    gold = await get_gold_price()
    return f'''
<html dir="rtl"><head><title>المشتري</title><style>body{{background:#0f172a;color:white;font-family:Tahoma;padding:20px;}}.box{{background:#1e293b;padding:20px;border-radius:12px;margin:10px 0;}}.btn{{background:#fbbf24;color:#0f172a;padding:10px 20px;border:none;border-radius:8px;cursor:pointer;}}</style></head>
<body><h1>🛒 مرحباً {user["name"]} (مشتري)</h1>
<div class="box"><a href="/buyer/create-order"><button class="btn">➕ إنشاء طلب شراء</button></a></div>
<div class="box"><h3>طلباتي</h3><p style="color:#94a3b8;">لا توجد طلبات حالية</p></div>
<div class="box"><h3>عروض التجار</h3><p style="color:#94a3b8;">سيتم عرضها هنا</p></div>
<div><a href="/auth/logout">تسجيل الخروج</a> | <a href="/">الرئيسية</a></div>
</body></html>
'''

@router.get("/create-order", response_class=HTMLResponse)
async def create_order_page(request: Request):
    user = get_user_from_cookie(request)
    if not user or user["role"] != "buyer": return RedirectResponse("/auth/login", 302)
    gold = await get_gold_price()
    return f'''
<html dir="rtl"><head><title>طلب جديد</title><style>body{{background:#0f172a;color:white;font-family:Tahoma;padding:20px;}}.box{{max-width:500px;margin:auto;background:#1e293b;padding:30px;border-radius:12px;}}input,textarea{{width:100%;padding:8px;margin:5px 0;border-radius:8px;background:#0f172a;color:white;border:1px solid #334155;}}.btn{{background:#fbbf24;color:#0f172a;padding:10px;border:none;border-radius:8px;cursor:pointer;}}</style></head>
<body><div class="box"><h2>➕ طلب شراء</h2><form action="/api/orders/create" method="post"><input type="number" name="quantity" placeholder="الكمية (جرام)" required><input type="number" name="price" step="0.01" placeholder="السعر" value="{gold}" required><textarea name="notes" placeholder="ملاحظات"></textarea><button class="btn" type="submit">إرسال الطلب</button></form><a href="/buyer/">⬅️ العودة</a></div></body></html>
'''

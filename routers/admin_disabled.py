from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db.compat import get_user_from_cookie, users_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    user = get_user_from_cookie(request)
    if not user or user["role"] != "admin": return RedirectResponse("/auth/login", 302)
    user_list = "<br>".join([f"{email} → {u['name']} ({u['role']})" for email, u in users_db.items()])
    return f'''
<html dir="rtl"><head><title>المشرف</title><style>body{{background:#0f172a;color:white;font-family:Tahoma;padding:20px;}}.box{{background:#1e293b;padding:20px;border-radius:12px;margin:10px 0;}}</style></head>
<body><h1>⚙️ لوحة المشرف</h1>
<div class="box"><h3>المستخدمين</h3><p>{user_list}</p></div>
<div class="box"><h3>إضافة إعلان</h3><form><input placeholder="العنوان"><textarea placeholder="الوصف"></textarea><button type="submit">نشر</button></form></div>
<a href="/auth/logout">تسجيل الخروج</a> | <a href="/">الرئيسية</a>
</body></html>
'''

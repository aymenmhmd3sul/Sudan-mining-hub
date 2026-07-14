from fastapi import APIRouter, Request, HTTPException, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
import hashlib, secrets
from app.db.legacy_adapter import get_user, create_session, hash_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login", response_class=HTMLResponse)
async def login_page():
    return '''
<html dir="rtl"><head><title>دخول</title><style>body{background:#0f172a;color:white;font-family:Tahoma;padding:20px;}.box{max-width:400px;margin:auto;background:#1e293b;padding:30px;border-radius:12px;}input{width:100%;padding:8px;margin:5px 0;border-radius:8px;border:1px solid #334155;background:#0f172a;color:white;}.btn{background:#fbbf24;color:#0f172a;padding:10px 20px;border:none;border-radius:8px;cursor:pointer;}</style></head>
<body><div class="box"><h2>🔐 تسجيل الدخول</h2><form action="/auth/login" method="post"><input type="email" name="email" placeholder="البريد" required><input type="password" name="password" placeholder="كلمة المرور" required><button class="btn" type="submit">دخول</button></form><a href="/auth/register">ليس لديك حساب؟ سجل الآن</a></div></body>
</html>
'''

@router.post("/login")
async def login(request: Request):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    user = get_user(email)
    if not user or user["password"] != hash_password(password):
        return HTMLResponse("بيانات غير صحيحة", status_code=401)
    token = create_session(email)
    resp = RedirectResponse("/", 302)
    resp.set_cookie("session_token", token, httponly=True)
    return resp

@router.get("/register", response_class=HTMLResponse)
async def register_page():
    return '''
<html dir="rtl"><head><title>تسجيل</title><style>body{background:#0f172a;color:white;font-family:Tahoma;padding:20px;}.box{max-width:400px;margin:auto;background:#1e293b;padding:30px;border-radius:12px;}input,select{width:100%;padding:8px;margin:5px 0;border-radius:8px;border:1px solid #334155;background:#0f172a;color:white;}.btn{background:#fbbf24;color:#0f172a;padding:10px 20px;border:none;border-radius:8px;cursor:pointer;}</style></head>
<body><div class="box"><h2>📝 إنشاء حساب</h2><form action="/auth/register" method="post"><input type="text" name="name" placeholder="الاسم" required><input type="email" name="email" placeholder="البريد" required><input type="password" name="password" placeholder="كلمة المرور" required><select name="role"><option value="buyer">مشتري</option><option value="seller">تاجر</option></select><button class="btn" type="submit">تسجيل</button></form><a href="/auth/login">لديك حساب؟ سجل دخول</a></div></body>
</html>
'''

@router.post("/register")
async def register(request: Request):
    form = await request.form()
    name = form.get("name"); email = form.get("email"); password = form.get("password"); role = form.get("role")
    if not email or not password: return HTMLResponse("بيانات ناقصة", 400)
    if get_user(email): return HTMLResponse("البريد موجود مسبقاً", 400)
    users_db[email] = {"name": name, "password": hash_password(password), "role": role}
    token = create_session(email)
    resp = RedirectResponse("/", 302)
    resp.set_cookie("session_token", token, httponly=True)
    return resp

@router.get("/logout")
async def logout():
    resp = RedirectResponse("/")
    resp.delete_cookie("session_token")
    return resp

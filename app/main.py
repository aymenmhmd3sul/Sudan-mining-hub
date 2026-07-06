import os
import pathlib
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent.parent
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import jwt

from app.database import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM

app = FastAPI(title="Sudan Mining Hub")

# إعداد المجلدات الثابتة والقوالب
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Dependency: التحقق من الهوية واستخراج المستخدم الحالي من الـ Cookie ---
async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="غير مسجل دخول")
    
    # تنظيف بادئة Bearer إذا وجدت
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="توكن غير صالح")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="انتهت صلاحية الجلسة")
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="المستخدم غير موجود")
    return user

# --- الواجهات الرسومية (Views) ---

@app.get("/")
@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    # إذا كان العميل مسجل دخول بالفعل، وجهه فوراً للوحة التحكم
    if request.cookies.get("access_token"):
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login_master.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_route(request: Request, current_user: User = Depends(get_current_user)):
    # حماية المسار: فقط من يحمل دور ADMIN يمكنه الرؤية
    user_roles = [role.name for role in current_user.roles]
    if "ADMIN" not in user_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="غير مصرح لك بدخول لوحة التحكم")
        
    return templates.TemplateResponse(request=request, name="admin.html", context={"user": current_user})

# --- مسارات العمليات الخلفية (API Endpoints) ---

@app.post("/api/auth/login")
async def login(
    response_class=RedirectResponse,
    username: str = Form(...),  # يستقبل الـ Form اسم المستخدم (الايميل) هنا
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # البحث عن المستخدم
    user = db.query(User).filter(User.email == username).first()
    if not user or not verify_password(password, user.hashed_password):
        # في حال الخطأ نرجعه لصفحة اللوجن مع رسالة خطأ (أو ارجاع استثناء مناسب)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="البريد الإلكتروني أو كلمة المرور غير صحيحة")
    
    # استخراج الأدوار
    roles = [role.name for role in user.roles]
    
    # توليد التوكن
    access_token = create_access_token(subject=user.email, roles=roles)
    
    # توجيه المستخدم للوحة التحكم وحقن التوكن في الـ Cookie أمنياً
    response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,  # حماية ضد هجمات XSS
        max_age=60 * 60 * 24, # يوم كامل
        samesite="lax"
    )
    return response

@app.get("/api/auth/logout")
async def logout():
    # تسجيل الخروج بمسح الـ Cookie التلقائي
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

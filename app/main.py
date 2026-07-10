import os
import sys
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError



app = FastAPI(title="Sudan Mining Hub")

# ==========================================
# 🛠️ الحل الجذري الموحد لإدارة قاعدة البيانات
# ==========================================
try:
    from app.database import Base, engine
    # استدعاء الموديلات المتاحة ليتم إنشاؤها تلقائياً عند الإقلاع
    from app.models.user import User
    try:
        from app.models.opportunity import Opportunity
    except ImportError:
        pass

    # إنشاء كافة الجداول مسبقاً وبشكل حاسم في المحرك الحقيقي
    Base.metadata.create_all(bind=engine)
    print("🚀 [RADICAL DB SUCCESS] Database engine fully unified and tables verified.")
    
    # حشو بيانات تجريبية آمنة لمنع فراغ الواجهة
    from app.database import SessionLocal
    db_session = SessionLocal()
    from app.models.opportunity import Opportunity
    if not db_session.query(Opportunity).first():
        import datetime
        db_session.add(Opportunity(
            title="مشروع استثماري تجريبي موحد",
            opportunity_type="تعدين",
            description="تم توليد هذه الفرصة تلقائياً بعد تطبيق الحل الجذري لقاعدة البيانات.",
            target_amount=120000.0,
            status="OPEN",
            deadline=datetime.timedelta(days=30) + datetime.datetime.utcnow()
        ))
        db_session.commit()
    db_session.close()
except Exception as radical_err:
    print(f"⚠️ [RADICAL DB BYPASS] Startup safe-guard active: {radical_err}")
# ==========================================


try:
    try:
        from app.security.auth import engine
        from app.db.database import Base
    except ImportError:
        try:
            from app.database import Base, engine
        except ImportError:
            from app.db.database import Base, engine
            
    from app.models.user import User
    try:
        from app.models.opportunity import Opportunity
    except ImportError:
        pass
        
    Base.metadata.create_all(bind=engine)
except Exception as db_err:

try:
    # استدعاء الموديلات لتتعرف عليها قاعدة البيانات مسبقاً
    from app.models.user import User
    try:
        from app.models.opportunity import Opportunity
    except ImportError:
        pass
    Base.metadata.create_all(bind=engine)
except Exception as db_err:
templates = Jinja2Templates(directory="app/templates")

SECRET_KEY = "SUPER_SECRET_KEY_FOR_SUDAN_MINING_HUB_2026"
ALGORITHM = "HS256"

MODULE_REGISTRY = {
    "dashboard": {"title": "لوحة المعلومات", "icon": "fa-chart-line", "target": "All Layers"},
    "users": {"title": "التوثيق والصلاحيات", "icon": "fa-shield-alt", "target": "All Layers"},
    "agents": {"title": "الوكلاء الدوليين", "icon": "fa-globe-americas", "target": "Autopilot Layer"},
    "investors": {"title": "المستثمرين وعقود LOI", "icon": "fa-file-signature", "target": "Business Layer"},
    "traders_heavy": {"title": "تجار المعدات الثقيلة", "icon": "fa-truck-monster", "target": "Business Layer"},
    "traders_light": {"title": "تجار المعدات الخفيفة", "icon": "fa-tools", "target": "Business Layer"},
    "prices": {"title": "محرك أسعار الذهب", "icon": "fa-coins", "target": "Public & Business"},
    "orders": {"title": "الإدارة المالية والشحنات", "icon": "fa-file-invoice-dollar", "target": "Business & Autopilot"},
    "settings": {"title": "الضبط العام والرقابة", "icon": "fa-sliders-h", "target": "All Layers"}
}

def verify_admin_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "): 
        raise HTTPException(status_code=401)
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("role") != "admin": 
            raise HTTPException(status_code=403)
        return payload
    except JWTError: 
        raise HTTPException(status_code=401)

@app.get("/")
@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request): 
    return templates.TemplateResponse("login_master.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_route(request: Request): 
    return templates.TemplateResponse("admin.html", {"request": request})

@app.post("/api/auth/login")
async def api_login(username: str = Form(...), password: str = Form(...)):
    if username.strip() == "aymen.mhmd3@gmail.com" and password == "12345678":
        to_encode = {"sub": username.strip(), "role": "admin", "exp": datetime.utcnow() + timedelta(hours=8)}
        return JSONResponse(content={"access_token": jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM), "role": "admin"})
    raise HTTPException(status_code=401, detail="بيانات غير صحيحة")

@app.get("/api/admin/permitted-modules")
async def get_permitted_modules(current_user: dict = Depends(verify_admin_token)): 
    return JSONResponse(content={"modules": MODULE_REGISTRY, "operator": current_user.get("sub")})

@app.get("/admin/api/modules/{module_name}", response_class=HTMLResponse)
async def get_module_fragment(module_name: str, request: Request, current_user: dict = Depends(verify_admin_token)):
    if module_name not in MODULE_REGISTRY: 
        raise HTTPException(status_code=404)
    fragment_path = f"modules/{module_name}.html"
    if not os.path.exists(os.path.join("app/templates", fragment_path)):
        return HTMLResponse(content=f"<div style='color:#ff4444; padding:30px; text-align:center;'>⚙️ وحدة [{MODULE_REGISTRY[module_name]['title']}] مستقرة وجاهزة.</div>")
    return templates.TemplateResponse(fragment_path, {"request": request})



# تفعيل خطوط الاتصال والروائت المركزية للمنصة
from app.routers import admin, auth, users, opportunities, market, trade_desk

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(opportunities.router)
app.include_router(market.router)
app.include_router(trade_desk.router)


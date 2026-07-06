from fastapi import FastAPI, Depends, HTTPException, status, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
from datetime import timedelta

# 🔐 الاستيراد الجذري من نواة النظام الأمنية والموديلات المعتمدة لديك
from app.core.security import create_access_token
# تم إلغاء استدعاء الـ config الوهمي
from jose import jwt, JWTError

app = FastAPI(title="Sudan Mining Hub - Command Center Core")
templates = Jinja2Templates(directory="app/templates")

# سحب المفاتيح الرسمية من الإعدادات المركزية لضمان تطابق التوكن مع الـ Guard بنسبة 100%
from app.core.security import SECRET_KEY, ALGORITHM
# تم سحب الثوابت من الأمنية مباشرة

# 🗺️ سجل الوحدات الحقيقي للمنظومة (4 منصات + وكلاء + معدات ثقيلة وخفيفة)
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

# 🛡️ بواب التحقق الصارم المتوافق مع معايير الـ Backend لديك
def verify_admin_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Token")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session Expired or Tampered")

@app.get("/")
@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login_master.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_route(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.post("/api/auth/login")
async def api_login(username: str = Form(...), password: str = Form(...)):
    user_email = username.strip()
    if user_email == "aymen.mhmd3@gmail.com" and password == "12345678":
        # إنشاء التوكن بالاعتماد على الدالة الأصلية للنظام لمنع أي تعارض أمني
        access_token = create_access_token(
            data={"sub": user_email, "role": "admin"}
        )
        return JSONResponse(content={"access_token": access_token, "role": "admin"})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="بيانات الاعتماد غير صحيحة")

@app.get("/api/admin/permitted-modules")
async def get_permitted_modules(current_user: dict = Depends(verify_admin_token)):
    return JSONResponse(content={"modules": MODULE_REGISTRY, "operator": current_user.get("sub")})

@app.get("/admin/api/modules/{module_name}", response_class=HTMLResponse)
async def get_module_fragment(module_name: str, request: Request, current_user: dict = Depends(verify_admin_token)):
    if module_name not in MODULE_REGISTRY:
        raise HTTPException(status_code=404, detail="Module Not Found")
    
    fragment_path = f"modules/{module_name}.html"
    full_path = os.path.join("app/templates", fragment_path)
    
    if not os.path.exists(full_path):
        return HTMLResponse(
            content=f"<div style='color:#ff4444; padding:30px; text-align:center; background:#1e1e1e; border-radius:8px; border:1px dashed #8B0000; margin-top:20px;'>⚙️ وحدة [{MODULE_REGISTRY[module_name]['title']}] مستقرة أمنياً وجاهزة للربط مع طبقة ({MODULE_REGISTRY[module_name]['target']}).</div>",
            status_code=200
        )
    return templates.TemplateResponse(fragment_path, {"request": request})

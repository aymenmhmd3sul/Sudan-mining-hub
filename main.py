from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
from datetime import datetime
from routers import auth, buyer, seller, admin, api

app = FastAPI(title="منصة السودان للتعدين")

# تضمين الراوترات
app.include_router(auth.router)
app.include_router(buyer.router)
app.include_router(seller.router)
app.include_router(admin.router)
app.include_router(api.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>منصة السودان للتعدين</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:Tahoma, Arial, sans-serif; background:#0f172a; color:#f1f5f9; min-height:100vh; padding:20px; }
.container { max-width:800px; margin:auto; }
.box { background:#1e293b; padding:30px; border-radius:16px; margin:15px 0; text-align:center; }
.btn { display:inline-block; padding:12px 30px; background:#fbbf24; color:#0f172a; text-decoration:none; border-radius:30px; font-weight:bold; margin:5px; }
.btn-blue { background:#3b82f6; color:white; }
</style>
</head>
<body>
<div class="container">
<div class="box"><h1>⛏️ منصة السودان للتعدين</h1><p>نظام إدارة طلبات الذهب</p></div>
<div class="box"><a href="/auth/login" class="btn btn-blue">تسجيل الدخول</a> <a href="/auth/register" class="btn">إنشاء حساب</a></div>
<div class="box" style="color:#94a3b8;">🟢 النظام مباشر</div>
</div>
</body>
</html>
'''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from app.routers import auth, users

app = FastAPI(title="Sudan Mining Hub")

# ربط الراوترات الموجودة والمستقرة فقط
app.include_router(auth.router, prefix="/api/auth")
app.include_router(users.router)

@app.get("/")
def root():
    return {"status": "running", "project": "Sudan Mining Hub"}

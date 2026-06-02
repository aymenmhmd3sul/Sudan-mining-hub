
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import engine, get_db
import uvicorn
import os

# إنشاء الجداول تلقائياً في PostgreSQL عند بدء التشغيل
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sudan Mining Hub API")

@app.get("/")
def read_root():
    return {"status": "running", "database": "connected"}

# 1. تسجيل مستخدم جديد وحفظه في قاعدة البيانات
@app.post("/api/v1/register", status_code=status.HTTP_201_CREATED)
def register_user(username: str, email: str, full_name: str = None, db: Session = Depends(get_db)):
    # التحقق من عدم تكرار اسم المستخدم
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # التحقق من عدم تكرار البريد الإلكتروني
    db_email = db.query(models.User).filter(models.User.email == email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # إضافة المستخدم الجديد
    new_user = models.User(username=username, email=email, full_name=full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user": {"id": new_user.id, "username": new_user.username}}

# 2. قراءة بيانات المستخدم حية من قاعدة البيانات
@app.get("/api/v1/profile/{username}")
def get_user_profile(username: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "source": "PostgreSQL Database",
        "profile": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "is_active": db_user.is_active
        }
    }

# تشغيل السيرفر وقراءة المنفذ الديناميكي الخاص بـ Render تلقائياً
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

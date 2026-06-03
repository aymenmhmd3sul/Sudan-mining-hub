from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import models
from database import engine, get_db

SECRET_KEY = "SUDAN_MINING_SUPER_SECRET_KEY_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

models.Base.metadata.create_all(bind=engine)

# إنشاء التطبيق مع تسمية عربية كاملة للواجهة
app = FastAPI(
    title="منصة التعدين السودانية",
    description="بوابة برمجية متكاملة لإدارة المستخدمين والصلاحيات والملفات الأمنية",
    version="1.0.0"
)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="لم يتم التحقق من الهوية، التوكن غير صالح",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/", tags=["الحالة العامة"])
def read_root():
    """التحقق من اتصال الخادم وقاعدة البيانات"""
    return {"status": "running", "database": "connected"}


# --- النافذة 1: تسجيل حساب جديد ---
@app.post("/api/v1/register", status_code=status.HTTP_201_CREATED, tags=["إدارة الحسابات"])
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    """
    **تسجيل مستخدم جديد في النظام:**
    - **username**: اسم المستخدم الفريد
    - **email**: البريد الإلكتروني الخاص بك
    - **password**: كلمة المرور السرية
    """
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجل بالفعل")
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="اسم المستخدم مأخوذ من قبل")
    
    hashed_pwd = pwd_context.hash(password)
    new_user = models.User(username=username, email=email, hashed_password=hashed_pwd, role="viewer")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "تم إنشاء الحساب بنجاح", "user_id": new_user.id}


# --- النافذة 2: تسجيل الدخول ---
@app.post("/api/v1/login", tags=["إدارة الحسابات"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    **تسجيل الدخول والحصول على مفتاح الأمان (Token):**
    - يرجى إدخال اسم المستخدم وكلمة المرور للحصول على صلاحية تصفح النظام الموثق.
    """
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="اسم المستخدم أو كلمة المرور غير صحيحة")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# --- النافذة 3: الملف الشخصي ---
@app.get("/api/v1/profile", tags=["بيانات المستخدم"])
def get_profile(current_user: models.User = Depends(get_current_user)):
    """
    **استعراض الملف الشخصي للمستخدِم الحالي:**
    - يتطلب تمرير توكن الأمان لرؤية رتبتك وصلاحياتك داخل النظام.
    """
    return {
        "المعرف": current_user.id,
        "اسم_المستخدم": current_user.username,
        "البريد_الإلكتروني": current_user.email,
        "الرتبة_الصلاحية": current_user.role,
        "تاريخ_الإنشاء": current_user.created_at
    }


# --- النافذة 4: تحديث الصلاحيات ---
@app.put("/api/v1/update-role", tags=["إدارة المشرفين"])
def update_user_role(target_username: str, new_role: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    **تعديل رتبة وصلاحيات مستخدم (خاص بالمسؤولين Admin فقط):**
    - **new_role**: الخيارات المتاحة هي (admin, supervisor, agent, viewer)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ليست لديك الصلاحية الكافية لتعديل الرتب")
    
    user_to_update = db.query(models.User).filter(models.User.username == target_username).first()
    if not user_to_update:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    
    if new_role not in ["admin", "supervisor", "agent", "viewer"]:
        raise HTTPException(status_code=400, detail="الرتبة المحددة غير صالحة")
        
    user_to_update.role = new_role
    db.commit()
    return {"message": f"تم تحديث صلاحية {target_username} بنجاح إلى {new_role}"}

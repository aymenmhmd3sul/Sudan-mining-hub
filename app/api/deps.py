from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, AsyncGenerator
from app.infrastructure.database import AsyncSessionLocal

# إعدادات افتراضية للتشفير لعام 2026
SECRET_KEY = "SUDAN_MINING_HUB_SUPER_SECRET_KEY_2026"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# الدالة المفقودة: توليد وحقن جلسة قاعدة البيانات بشكل آمن وتلقائي الإغلاق
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """توليد جلسة قاعدة بيانات غير متزامنة لكل طلب وإغلاقها تلقائياً بعد الانتهاء"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """فك التوكن والتحقق من هوية المستخدم وصلاحيته الحالية"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="لم يتم التحقق من صحة الاعتماديات أو انتهت صلاحية الجلسة",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        role: str = payload.get("role")
        username: str = payload.get("username")
        
        if user_id is None or role is None:
            raise credentials_exception
        return {"id": user_id, "role": role, "username": username}
    except JWTError:
        raise credentials_exception

class RoleChecker:
    """فاحص ديناميكي للأدوار لمنع العبور العشوائي (RBAC)"""
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
        
    def __call__(self, current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"غير مسموح لك بالوصول! هذه العملية مخصصة للأدوار التالية فقط: {self.allowed_roles}"
            )
        return current_user


from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
import os
from app.routers.admin_control import get_current_admin

router = APIRouter(prefix="/admin/api/modules", tags=["Admin Modules Loader"])

@router.get("/{module_name}", response_class=HTMLResponse)
async def load_module_template(module_name: str, current_admin: dict = Depends(get_current_admin)):
    """
    يقوم هذا المسار بقراءة ملف الـ HTML الخاص بالوحدة المطلوبة
    وإرساله للواجهة كـ Fragment بعد التحقق من صحة توكن الإدارة.
    """
    file_path = f"app/templates/modules/{module_name}.html"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Module Template Not Found")
    
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    return html_content

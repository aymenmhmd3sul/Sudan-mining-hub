from fastapi import APIRouter, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

# 🎯 التعديل الصحيح: استدعاء النواة وقاعدة البيانات من مسارها الفعلي في المشروع
from app.database import get_db 
from app.services.admin_services import AdminOperationsService

router = APIRouter(
    prefix="/admin/operations",
    tags=["Operations & Control Center"]
)

# 1. الرئيسية: جلب الإحصائيات الحية
@router.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    try:
        stats = AdminOperationsService.get_live_dashboard_stats(db)
        return {"status": "success", "data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في جلب الإحصائيات الحية: {str(e)}")

# 2. مركز الإعدادات المالية
@router.post("/financials/update-config")
def update_financial_config(
    bankak_account: str = Form(...),
    local_wallets: str = Form(...),
    foreign_accounts: str = Form(...),
    trade_fee_percent: float = Form(...),
    subscription_price: float = Form(...),
    db: Session = Depends(get_db)
):
    success = AdminOperationsService.update_financial_settings(
        db, bankak_account, local_wallets, foreign_accounts, trade_fee_percent, subscription_price
    )
    if success:
        return {"status": "success", "message": "✅ تم تحديث مركز الإعدادات المالية بنجاح!"}
    raise HTTPException(status_code=400, detail="فشل تحديث الإعدادات المالية.")

# 3. إدارة المحتوى ديناميكياً
@router.post("/content/update-homepage")
def update_homepage_content(
    ticker_gold_price: str = Form(...),
    announcement_text: str = Form(...),
    active_banner_url: str = Form(...),
    db: Session = Depends(get_db)
):
    success = AdminOperationsService.update_system_content(
        db, ticker_gold_price, announcement_text, active_banner_url
    )
    if success:
        return {"status": "success", "message": "✨ تم تحديث محتوى الصفحة الرئيسية والتنبيهات!"}
    raise HTTPException(status_code=400, detail="فشل تحديث محتوى الإدارة.")

# 4. المستخدمون والقدرات
@router.post("/users/{user_id}/modify-capability")
def modify_user_capability(
    user_id: int, 
    capability: str = Form(...),
    action: str = Form(...),     
    db: Session = Depends(get_db)
):
    updated_user = AdminOperationsService.toggle_user_capability(db, user_id, capability, action)
    if updated_user:
        return {"status": "success", "message": f"تم بنجاح {action} القدرة [{capability}] للمستخدم {user_id}"}
    raise HTTPException(status_code=404, detail="المستخدم غير موجود.")

# 5. مراجعة البلاغات الجارية
@router.get("/marketplace/reported-ads")
def get_reported_ads(db: Session = Depends(get_db)):
    reported_items = AdminOperationsService.get_all_reported_ads(db)
    return {"status": "success", "items": reported_items}

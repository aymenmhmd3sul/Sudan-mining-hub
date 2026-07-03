from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.db import get_db_connection
from app.core.dependencies import require_admin

router = APIRouter(tags=["Admin Dashboard Core"])

class AssetReviewPayload(BaseModel):
    status: str  # يجب أن تكون 'PUBLISHED' أو 'REJECTED'
    rejection_reason: str = None

@router.post("/assets/{asset_id}/review")
def review_mining_asset(asset_id: int, payload: AssetReviewPayload, current_user: dict = Depends(require_admin)):
    """مراجعة واعتماد أو رفض أصول التعدين المعلقة (خاص بالـ Super Admin فقط)."""
    if payload.status not in ["PUBLISHED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="الحالة المطلوبة غير صحيحة. يجب أن تكون PUBLISHED أو REJECTED")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # التأكد من وجود الأصل أولاً
    asset = cursor.execute("SELECT * FROM mining_assets WHERE id = ?", (asset_id,)).fetchone()
    if not asset:
        conn.close()
        raise HTTPException(status_code=404, detail="أصل التعدين المحدد غير موجود")
        
    # تحديث حالة الأصل في قاعدة البيانات
    cursor.execute(
        "UPDATE mining_assets SET state = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (payload.status, asset_id)
    )
    
    # 🔔 مكافأة معمارية: توليد إشعار تلقائي لصاحب الأصل لإعلامه بالقرار الإداري
    asset_dict = dict(asset)
    msg = f"تمت الموافقة على نشر إعلانك: ({asset_dict['title']}) وهو الآن نشط في السوق." if payload.status == "PUBLISHED" else f"عذراً، تم رفض إعلانك بسبب: {payload.rejection_reason}"
    
    cursor.execute(
        "INSERT INTO notifications (user_id, title, message) VALUES (?, ?, ?)",
        (asset_dict["owner_id"], "📢 تحديث حالة الإعلان", msg)
    )
    
    conn.commit()
    conn.close()
    
    return {"message": f"تم تحديث حالة الأصل بنجاح إلى {payload.status} وإشعار المالك برمجياً."}

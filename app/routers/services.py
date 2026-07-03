from fastapi import APIRouter, Depends, HTTPException, status
from app.core.db import get_db_connection
from app.core.dependencies import require_any_user

router = APIRouter(tags=["Supporting Services"])

@router.get("/notifications")
def get_my_notifications(current_user: dict = Depends(require_any_user)):
    """استرجاع كافة الإشعارات الخاصة بالمستخدم الحالي."""
    conn = get_db_connection()
    notifications = conn.execute(
        "SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC",
        (current_user["id"],)
    ).fetchall()
    conn.close()
    
    return [dict(n) for n in notifications]

@router.post("/notifications/{notif_id}/read")
def mark_as_read(notif_id: int, current_user: dict = Depends(require_any_user)):
    """تحديث حالة الإشعار إلى مقروء."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # التأكد من أن الإشعار يخص المستخدم نفسه حمايةً للبيانات
    notif = cursor.execute("SELECT * FROM notifications WHERE id = ? AND user_id = ?", 
                           (notif_id, current_user["id"])).fetchone()
    if not notif:
        conn.close()
        raise HTTPException(status_code=404, detail="الإشعار غير موجود أو غير تابع لك")
        
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
    conn.commit()
    conn.close()
    return {"message": "تم تحديث الإشعار إلى مقروء"}

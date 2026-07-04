from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.api.deps import get_db_session
from app.infrastructure.models.interactions import AssetReport
from app.infrastructure.models.core import MiningAsset

router = APIRouter(prefix="/reports", tags=["Reports & Moderation"])

class ReportCreatePayload(BaseModel):
    asset_id: int = Field(..., description="معرف الإعلان المشكو في حقه")
    reporter_id: int = Field(..., description="معرف المستخدم المبلّغ")
    reason: str = Field(..., min_length=5, description="سبب البلاغ تفصيلياً (احتيال، تم البيع، بيانات خاطئة)")

@router.post("/submit", status_code=status.HTTP_201_CREATED)
async def submit_asset_report(payload: ReportCreatePayload, db: AsyncSession = Depends(get_db_session)):
    """
    مبدأ الإدارة بالاستثناء:
    استقبال البلاغ، وحظر الإعلان مؤقتاً أو نقله للمراجعة آلياً إذا تراكمت الشكاوى.
    """
    # 1. التحقق من وجود الإعلان أولاً
    asset_stmt = select(MiningAsset).where(MiningAsset.id == payload.asset_id)
    asset_res = await db.execute(asset_stmt)
    asset = asset_res.scalars().first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="الإعلان المستهدف غير موجود في النظام.")

    # 2. تسجيل البلاغ الجديد في قاعدة البيانات
    new_report = AssetReport(
        asset_id=payload.asset_id,
        reporter_id=payload.reporter_id,
        reason=payload.reason,
        status="PENDING"
    )
    db.add(new_report)
    await db.flush() # الحصول على ID البلاغ دون عمل Commit كامل للعملية

    # 3. حساب عدد الشكاوى المعلقة ضد هذا الإعلان لمعرفة هل تخطينا حد الأمان
    count_stmt = select(func.count(AssetReport.id)).where(
        AssetReport.asset_id == payload.asset_id,
        AssetReport.status == "PENDING"
    )
    count_res = await db.execute(count_stmt)
    active_reports_count = count_res.scalar() or 0

    # حد الحماية الأوتوماتيكي للسوق (الإدارة بالاستثناء)
    TRIGGER_REVIEW_LIMIT = 3
    auto_moderated = False

    if active_reports_count >= TRIGGER_REVIEW_LIMIT and asset.status == "APPROVED":
        # نقل الإعلان لطاولة الفحص البشري تلقائياً دون إغلاق حساب البائع
        asset.status = "UNDER_REVIEW"
        auto_moderated = True
    
    await db.commit()

    return {
        "message": "📥 تم استلام بلاغك بنجاح وجاري تدقيقه من قبل النظام الآلي.",
        "report_id": new_report.id,
        "active_reports_on_asset": active_reports_count,
        "auto_moderated": auto_moderated,
        "current_asset_status": asset.status
    }

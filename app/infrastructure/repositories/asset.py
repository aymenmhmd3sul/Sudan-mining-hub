from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.infrastructure.models.core import MiningAsset
from app.infrastructure.models.extensions import AssetLocation, AssetSpec

class AssetRepository:
    def __init__(self, db_session):
        self.db = db_session

    async def get_by_id(self, asset_id: int) -> Optional[MiningAsset]:
        """ جلب الأصل التعديني بكافة تفاصيله الجغرافية والفنية عبر معرفه """
        stmt = select(MiningAsset).options(selectinload(MiningAsset.locations)).where(MiningAsset.id == asset_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_asset_with_details(
        self, asset_data: Dict[str, Any], location_data: Dict[str, Any], specs_data: List[Dict[str, Any]]
    ) -> MiningAsset:
        """ إنشاء أصل تعديني جديد مع ربط جغرافي وفني كامل في عملية موحدة """
        asset = MiningAsset(**asset_data)
        self.db.add(asset)
        await self.db.flush()
        
        location = AssetLocation(asset_id=asset.id, **location_data)
        self.db.add(location)
        
        for spec in specs_data:
            specification = AssetSpec(asset_id=asset.id, **spec)
            self.db.add(specification)
            
        await self.db.flush()
        return asset

    async def search_assets_advanced(self, criteria) -> Tuple[List[MiningAsset], int]:
        """ تنفيذ استعلام البحث الديناميكي فائق الأداء لعام 2026 مدمجاً معه أوضاع ترتيب السوق الذكي. """
        # استخدام selectinload لضمان جلب بيانات الموقع جغرافياً ومنع خطأ MissingGreenlet
        stmt = select(MiningAsset).options(selectinload(MiningAsset.locations)).join(MiningAsset.locations)

        # تطبيق مجموعات الفلاتر (Filters Groups)
        if criteria.status:
            stmt = stmt.where(MiningAsset.status == criteria.status)
        if criteria.category_id:
            stmt = stmt.where(MiningAsset.category_id == criteria.category_id)

        # فلاتر الموقع الجغرافي
        if criteria.state:
            stmt = stmt.where(AssetLocation.state == criteria.state)
        if criteria.region:
            stmt = stmt.where(AssetLocation.region == criteria.region)

        # حساب العدد الإجمالي الفعلي قبل الـ Pagination
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_count_res = await self.db.execute(count_stmt)
        total_count = total_count_res.scalar() or 0

        # تطبيق منطق أوضاع ترتيب السوق ديناميكياً
        sort_mode = getattr(criteria, 'sort_by', 'MARKET_FLOW')
        if sort_mode == "TRUSTED_FIRST":
            stmt = stmt.order_by(MiningAsset.trust_score.desc(), MiningAsset.created_at.desc())
        elif sort_mode == "INVESTOR_VIEW":
            stmt = stmt.order_by(MiningAsset.trust_score.desc(), MiningAsset.views_count.desc())
        else:
            stmt = stmt.order_by(MiningAsset.created_at.desc(), MiningAsset.views_count.desc())

        # تطبيق الـ Pagination الصارم
        offset = (criteria.page - 1) * criteria.limit
        stmt = stmt.offset(offset).limit(criteria.limit)

        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total_count

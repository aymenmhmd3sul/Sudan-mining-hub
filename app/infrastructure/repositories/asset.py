from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.infrastructure.models.core import MiningAsset
from app.infrastructure.models.extensions import AssetLocation, AssetSpec


class AssetRepository:
    def __init__(self, db_session):
        self.db = db_session

    async def get_by_id(
        self,
        asset_id: int,
    ) -> Optional[MiningAsset]:
        stmt = (
            select(MiningAsset)
            .options(
                selectinload(MiningAsset.locations),
                selectinload(MiningAsset.specs),
            )
            .where(MiningAsset.id == asset_id)
        )

        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_id_for_update(
        self,
        asset_id: int,
    ) -> Optional[MiningAsset]:
        stmt = (
            select(MiningAsset)
            .options(
                selectinload(MiningAsset.locations),
                selectinload(MiningAsset.specs),
            )
            .where(MiningAsset.id == asset_id)
            .with_for_update()
        )

        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_asset_with_details(
        self,
        asset_data: Dict[str, Any],
        location_data: Dict[str, Any],
        specs_data: List[Dict[str, Any]],
    ) -> MiningAsset:

        asset = MiningAsset(**asset_data)

        self.db.add(asset)
        await self.db.flush()

        location = AssetLocation(
            asset_id=asset.id,
            **location_data,
        )
        self.db.add(location)

        for spec in specs_data:
            self.db.add(
                AssetSpec(
                    asset_id=asset.id,
                    **spec,
                )
            )

        await self.db.flush()
        return asset

    async def search_assets_advanced(
        self,
        criteria,
    ) -> Tuple[List[MiningAsset], int]:

        filters = []

        if criteria.status:
            filters.append(
                MiningAsset.status == criteria.status
            )

        if criteria.category_id:
            filters.append(
                MiningAsset.category_id == criteria.category_id
            )

        if criteria.min_price is not None:
            filters.append(
                MiningAsset.price >= criteria.min_price
            )

        if criteria.max_price is not None:
            filters.append(
                MiningAsset.price <= criteria.max_price
            )

        if criteria.verified_only:
            filters.append(
                MiningAsset.is_verified.is_(True)
            )

        if criteria.has_mining_license:
            filters.append(
                MiningAsset.has_mining_license.is_(True)
            )

        location_required = (
            criteria.state is not None
            or criteria.region is not None
        )

        base = select(MiningAsset)

        if location_required:
            base = base.join(
                AssetLocation,
                AssetLocation.asset_id == MiningAsset.id,
            )

            if criteria.state:
                filters.append(
                    AssetLocation.state == criteria.state
                )

            if criteria.region:
                filters.append(
                    AssetLocation.region == criteria.region
                )

        if filters:
            base = base.where(*filters)

        count_stmt = select(
            func.count(func.distinct(MiningAsset.id))
        ).select_from(MiningAsset)

        if location_required:
            count_stmt = count_stmt.join(
                AssetLocation,
                AssetLocation.asset_id == MiningAsset.id,
            )

        if filters:
            count_stmt = count_stmt.where(*filters)

        total_result = await self.db.execute(count_stmt)
        total_count = int(total_result.scalar() or 0)

        if location_required:
            base = base.distinct()

        sort_mode = getattr(
            criteria,
            "sort_by",
            "MARKET_FLOW",
        )

        if sort_mode == "TRUSTED_FIRST":
            base = base.order_by(
                MiningAsset.trust_score.desc(),
                MiningAsset.created_at.desc(),
            )

        elif sort_mode == "INVESTOR_VIEW":
            base = base.order_by(
                MiningAsset.trust_score.desc(),
                MiningAsset.views_count.desc(),
                MiningAsset.created_at.desc(),
            )

        else:
            base = base.order_by(
                MiningAsset.created_at.desc(),
                MiningAsset.views_count.desc(),
            )

        offset = max(0, criteria.page - 1) * criteria.limit

        stmt = (
            base.options(
                selectinload(MiningAsset.locations),
                selectinload(MiningAsset.specs),
            )
            .offset(offset)
            .limit(criteria.limit)
        )

        result = await self.db.execute(stmt)

        return (
            list(result.scalars().unique().all()),
            total_count,
        )

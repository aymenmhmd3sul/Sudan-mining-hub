import time
from datetime import datetime, UTC
from typing import Optional, List, Dict, Any
from app.domain.services.ranking import MarketRankingEngine

class SearchCriteria:
    """ كائن نقي يمثل طلب ومعايير البحث المتقدم دون تداخل مع قاعدة البيانات """
    def __init__(
        self,
        state: Optional[str] = None,
        region: Optional[str] = None,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        status: Optional[str] = "APPROVED",
        verified_only: bool = False,
        has_mining_license: bool = False,
        sort_by: str = "MARKET_FLOW", # MARKET_FLOW, TRUSTED_FIRST, INVESTOR_VIEW
        page: int = 1,
        limit: int = 10
    ):
        self.state = state
        self.region = region
        self.category_id = category_id
        self.min_price = min_price
        self.max_price = max_price
        self.status = status
        self.verified_only = verified_only
        self.has_mining_license = has_mining_license
        self.sort_by = sort_by
        self.page = page
        self.limit = limit

class SearchResultMetadata:
    """ بيانات ذكاء تعديني مدمجة تصف أداء الاستعلام والفلاتر النشطة """
    def __init__(self, total_count: int, execution_time_ms: float, criteria: SearchCriteria):
        self.total_count = total_count
        self.execution_time_ms = execution_time_ms
        self.page = criteria.page
        self.limit = criteria.limit
        self.total_pages = (total_count + criteria.limit - 1) // criteria.limit if total_count > 0 else 1
        self.applied_filters = {
            "state": criteria.state,
            "region": criteria.region,
            "category_id": criteria.category_id,
            "view_mode": criteria.sort_by,
            "page": criteria.page
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_count": self.total_count,
            "total_pages": self.total_pages,
            "current_page": self.page,
            "limit": self.limit,
            "execution_time_ms": f"{self.execution_time_ms:.2f}ms",
            "applied_filters": self.applied_filters
        }

class SearchService:
    def __init__(self, asset_repo):
        self.asset_repo = asset_repo

    async def execute_advanced_search(self, criteria: SearchCriteria) -> Dict[str, Any]:
        """
        المايسترو المسؤول عن جلب الأصول وحقنها بلمسات السوق البشرية وحساب مؤشرات الذكاء التعديني.
        """
        start_time = time.perf_counter()
        
        # 1. استدعاء المستودع المحدث المعتمد على الترتيب الذكي لقواعد البيانات
        assets, total_count = await self.asset_repo.search_assets_advanced(criteria)
        
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000
        
        # 2. توليد التقرير الوصفي لبنية البيانات الوصفية
        meta = SearchResultMetadata(total_count, execution_time_ms, criteria)
        
        # 3. صياغة المخرجات وحقن الشارات والألقاب البشرية (Human-Centric Badges) لكل أصل
        formatted_results = []
        for asset in assets:
            # حساب النقاط اللحظية بناءً على وضع العرض الحالي لتوثيق الحساب
            score = MarketRankingEngine.calculate_asset_score(asset, view_mode=criteria.sort_by)
            # توليد الألقاب والمؤشرات المجتمعية اللطيفة
            badge_info = MarketRankingEngine.attach_human_badges(asset, score)
            
            formatted_results.append({
                "id": asset.id,
                "title": asset.title,
                "status": asset.status,
                "listing_tier": asset.listing_tier,
                "score_rank": score,
                "human_badge": badge_info["human_badge"],
                "trust_stars": badge_info["trust_indicator"],
                "state": asset.locations[0].state if asset.locations else "غير محدد",
                "region": asset.locations[0].region if asset.locations else "غير محدد",
                "created_at": asset.created_at.isoformat() if asset.created_at else None
            })
            
        # 4. إعادة ترتيب المصفوفة النهائية لضمان دقة دمج أوزان البث المباشر للأصول
        formatted_results.sort(key=lambda x: x["score_rank"], reverse=True)

        return {
            "metadata": meta.to_dict(),
            "results": formatted_results
        }

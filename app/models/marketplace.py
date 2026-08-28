"""
Compatibility facade.

MiningAsset MUST NOT be redefined here.
The canonical ORM model lives in app.infrastructure.models.core.
"""

from app.infrastructure.models.core import AssetType, MiningAsset

__all__ = ["AssetType", "MiningAsset"]

"""
Canonical infrastructure ORM model registry.

All infrastructure models share the single SQLAlchemy Base
defined by app.database.
"""

# IMPORTANT:
# User must be imported before models that declare
# relationship("User", ...), so SQLAlchemy can resolve the class
# during mapper configuration.
from app.models.user import User

# Core models
from app.infrastructure.models.core import (
    Category,
    AssetType,
    MiningAsset,
)

# Asset extensions
from app.infrastructure.models.extensions import (
    AssetLocation,
    AssetSpec,
    AssetImage,
    AssetDocument,
)

# Asset interaction/history models
from app.infrastructure.models.interactions import (
    AssetStatusHistory,
    AssetEvent,
    PriceHistory,
    AssetNegotiation,
    AssetReport,
    AssetFavorite,
    AssetView,
)

__all__ = [
    "User",
    "Category",
    "AssetType",
    "MiningAsset",
    "AssetLocation",
    "AssetSpec",
    "AssetImage",
    "AssetDocument",
    "AssetStatusHistory",
    "AssetEvent",
    "PriceHistory",
    "AssetNegotiation",
    "AssetReport",
    "AssetFavorite",
    "AssetView",
]

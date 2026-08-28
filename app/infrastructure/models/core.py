from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)


class AssetType(str, Enum):
    WELL = "well"
    MINE = "mine"
    PRODUCTION_LINE = "production_line"
    FACTORY_WORKSHOP = "factory_workshop"
    SHOP = "shop"
    HEAVY_EQUIPMENT = "heavy_equipment"
    LIGHT_EQUIPMENT = "light_equipment"
    PRODUCT = "product"
    OTHER = "other"


class MiningAsset(Base):
    """
    Canonical MiningAsset ORM model.

    This is the ONLY ORM mapping for mining_assets.
    app.models.marketplace imports this class for compatibility.
    """

    __tablename__ = "mining_assets"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    category_id = Column(Integer, nullable=True, index=True)

    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)

    asset_type = Column(
        String(50),
        nullable=False,
        default=AssetType.OTHER.value,
        index=True,
    )

    other_description = Column(String, nullable=True)

    main_category = Column(
        String(100),
        nullable=False,
        default="GENERAL",
    )

    sub_category = Column(
        String(100),
        nullable=False,
        default="GENERAL",
    )

    price = Column(Float, nullable=False)
    currency = Column(String(20), default="USD")
    is_negotiable = Column(Boolean, default=True)

    state_province = Column(String(150), nullable=False)
    locality = Column(String(150), nullable=False)
    coordinates = Column(String, nullable=True)

    images_urls = Column(String, nullable=True)
    specific_specs = Column(String, nullable=True)

    is_featured = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)

    status = Column(
        String(50),
        default="ACTIVE",
        index=True,
    )

    listing_tier = Column(
        String(30),
        default="OPEN",
        index=True,
    )

    trust_score = Column(
        Float,
        default=50.0,
        nullable=False,
        index=True,
    )

    views_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    favorites_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    has_mining_license = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_status_change_at = Column(DateTime, nullable=True)
    last_negotiation_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Optimistic Concurrency Control (OCC)
    # Must match the existing mining_assets.version database column.
    version = Column(
        Integer,
        default=1,
        nullable=False,
    )

    __mapper_args__ = {
        "version_id_col": version,
    }

    owner = relationship(
        "User",
        backref="assets",
        foreign_keys=[owner_id],
    )

    locations = relationship(
        "AssetLocation",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

    specs = relationship(
        "AssetSpec",
        back_populates="asset",
        cascade="all, delete-orphan",
    )


    # Interaction relationships
    status_history = relationship(
        "AssetStatusHistory",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

    events = relationship(
        "AssetEvent",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

    price_history = relationship(
        "PriceHistory",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

    negotiations = relationship(
        "AssetNegotiation",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

    reports = relationship(
        "AssetReport",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

    favorites = relationship(
        "AssetFavorite",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

    views = relationship(
        "AssetView",
        back_populates="asset",
        cascade="all, delete-orphan",
    )

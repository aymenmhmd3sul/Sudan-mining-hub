from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, String, Text, DateTime, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database import Base

class AssetStatusHistory(Base):
    __tablename__ = "asset_status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id", ondelete="CASCADE"), nullable=False)
    from_state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    to_state: Mapped[str] = mapped_column(String(50), nullable=False)
    actor: Mapped[str] = mapped_column(String(50), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    asset: Mapped["MiningAsset"] = relationship("MiningAsset", back_populates="status_history")


class AssetEvent(Base):
    __tablename__ = "asset_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id", ondelete="CASCADE"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # يخزن كـ JSON String
    actor: Mapped[str] = mapped_column(String(50), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    asset: Mapped["MiningAsset"] = relationship("MiningAsset", back_populates="events")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id", ondelete="CASCADE"), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="SDG")
    changed_by: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    asset: Mapped["MiningAsset"] = relationship("MiningAsset", back_populates="price_history")


class AssetNegotiation(Base):
    __tablename__ = "asset_negotiations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id", ondelete="CASCADE"), nullable=False)
    buyer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    current_offer_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    asset: Mapped["MiningAsset"] = relationship("MiningAsset", back_populates="negotiations")


class AssetReport(Base):
    __tablename__ = "asset_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id", ondelete="CASCADE"), nullable=False)
    reporter_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="PENDING")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    asset: Mapped["MiningAsset"] = relationship("MiningAsset", back_populates="reports")


class AssetFavorite(Base):
    __tablename__ = "asset_favorites"

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (PrimaryKeyConstraint("user_id", "asset_id"),)
    asset: Mapped["MiningAsset"] = relationship("MiningAsset", back_populates="favorites")


class AssetView(Base):
    __tablename__ = "asset_views"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id", ondelete="CASCADE"), nullable=False)
    viewer_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    asset: Mapped["MiningAsset"] = relationship("MiningAsset", back_populates="views")

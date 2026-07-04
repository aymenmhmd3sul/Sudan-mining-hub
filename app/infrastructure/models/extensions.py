from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from app.infrastructure.database import Base

class AssetLocation(Base):
    __tablename__ = "asset_locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id", ondelete="CASCADE"))
    state: Mapped[str] = mapped_column(String(100))
    region: Mapped[Optional[str]] = mapped_column(String(100))
    latitude: Mapped[Optional[str]] = mapped_column(String(50))
    longitude: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    asset = relationship("MiningAsset", back_populates="locations")

class AssetSpec(Base):
    __tablename__ = "asset_specs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id", ondelete="CASCADE"))
    spec_key: Mapped[str] = mapped_column(String(100))
    spec_value: Mapped[str] = mapped_column(Text)

    asset = relationship("MiningAsset", back_populates="specs")

class AssetDocument(Base):
    __tablename__ = "asset_documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id"))
    doc_url: Mapped[str] = mapped_column(String(255))

class AssetImage(Base):
    __tablename__ = "asset_images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("mining_assets.id"))
    image_url: Mapped[str] = mapped_column(String(255))

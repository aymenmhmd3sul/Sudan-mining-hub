from datetime import datetime
from typing import Optional
from enum import Enum
from sqlalchemy import String, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class UserRole(str, Enum):
    ADMIN = "admin"
    MERCHANT = "merchant"
    BUYER = "buyer"
    AGENT = "agent"

class UserStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[UserRole] = mapped_column(String(50), default=UserRole.BUYER, nullable=False)
    status: Mapped[UserStatus] = mapped_column(String(50), default=UserStatus.PENDING, nullable=False)
    country: Mapped[str] = mapped_column(String(10), default="SD", nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="ar", nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_moderator: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_seller: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_importer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_global_provider: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    @property
    def full_name(self) -> str:
        return self.name

    @property
    def hashed_password(self) -> str:
        return self.password_hash

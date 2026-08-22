from datetime import datetime
from typing import Optional
from enum import Enum
from sqlalchemy import String, DateTime, Boolean, Integer, event
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
    # Canonical DB identity name. Kept synchronized with name for legacy compatibility.
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Legacy database compatibility:
    # PostgreSQL still requires this historical column.
    # It must contain the same hash as password_hash for new users.
    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

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
    def display_name(self) -> str:
        return self.full_name or self.name


# ---------------------------------------------------------------------------
# Identity compatibility guard
# ---------------------------------------------------------------------------
# Every registration path (agent / merchant / buyer / future roles) passes
# through this ORM model. Synchronize the two historical identity columns
# before PostgreSQL receives the INSERT, preventing full_name NULL violations.
@event.listens_for(User, "before_insert")
def sync_user_identity_names(mapper, connection, target):
    name = (target.name or "").strip()
    full_name = (target.full_name or "").strip()

    if not name and full_name:
        target.name = full_name
        name = full_name

    if not full_name and name:
        target.full_name = name

    if not target.name or not target.full_name:
        raise ValueError("User requires a non-empty name/full_name")

    # Password compatibility bridge:
    # password_hash is canonical; hashed_password is retained
    # because the production PostgreSQL schema still requires it.
    if not target.password_hash and target.hashed_password:
        target.password_hash = target.hashed_password

    if target.password_hash and not target.hashed_password:
        target.hashed_password = target.password_hash

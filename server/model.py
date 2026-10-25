from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    Text,
    CheckConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from datetime import datetime


class Base(DeclarativeBase):
    pass

auth_users = Table(
    "users",
    Base.metadata,
    Column("id", UUID(as_uuid=False), primary_key=True),
    schema="auth",
    info={"external": True},
)
class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("auth.users.id"),
        primary_key=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False,
)

    url_scans: Mapped[list["URLScan"]] = relationship(back_populates="profile")



class URLScan(Base):
    __tablename__ = "url_scans"

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'completed', 'failed')",
            name="check_url_scan_status",
        ),
        CheckConstraint(
            "risk_level IN ('unknown', 'low', 'medium', 'high')",
            name="check_url_scan_risk_level",
        ),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("profiles.id"),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(20),
        default="unknown",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False,
)

    profile: Mapped["Profile"] = relationship(
        back_populates="url_scans",
    )

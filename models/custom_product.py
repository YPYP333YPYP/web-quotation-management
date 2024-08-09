from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, TEXT
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column


@dataclass
class CustomProduct(Base):
    __tablename__ = "custom_products"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(TEXT, nullable=True)
    category: Mapped[str] = mapped_column(String(255), index=True)
    unit: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.current_timestamp())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)


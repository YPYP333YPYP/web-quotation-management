from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import ForeignKey, Integer, DateTime, func
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class Quotation(Base):
    __tablename__ = 'quotations'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    client_id = mapped_column(Integer, ForeignKey('clients.id'), nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.current_timestamp())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    products = relationship("Product", secondary="quotation_product", back_populates="quotations")
    client = relationship("Client", back_populates="quotations")

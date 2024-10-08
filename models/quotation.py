from dataclasses import dataclass
from datetime import datetime, date

from sqlalchemy import ForeignKey, Integer, DateTime, func, String, Text, Date
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, class_mapper


@dataclass
class Quotation(Base):
    __tablename__ = 'quotations'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    client_id = mapped_column(Integer, ForeignKey('clients.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="CREATED", nullable=False)
    input_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.current_timestamp())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    particulars: Mapped[str] = mapped_column(Text, nullable=True)

    products = relationship("Product", secondary="quotation_product", back_populates="quotations")
    client = relationship("Client", back_populates="quotations")

    def to_dict(self):
        mapper = class_mapper(self.__class__)
        columns = [column.key for column in mapper.columns]
        return {column: getattr(self, column) for column in columns}


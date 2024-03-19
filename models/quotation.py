from dataclasses import dataclass
from typing import List

from sqlalchemy import ForeignKey
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class Quotation(Base):
    __tablename__ = 'quotations'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    client_id = mapped_column(ForeignKey('clients.id'), nullable=False)

    products = relationship("Product", secondary="quotation_product", back_populates="quotations")
    client = relationship("Client", back_populates="quotations")

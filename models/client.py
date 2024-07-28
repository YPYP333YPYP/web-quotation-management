from dataclasses import dataclass
from typing import List

from sqlalchemy import String, Text
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    region: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(String(255))
    comment: Mapped[str] = mapped_column(Text)
    quotations = relationship("Quotation", back_populates="client")
    users = relationship("User", back_populates="client")



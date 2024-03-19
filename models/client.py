from dataclasses import dataclass
from typing import List

from sqlalchemy import String
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    region: Mapped[str] = mapped_column(String(255))
    quotations = relationship("Quotation", back_populates="clients")

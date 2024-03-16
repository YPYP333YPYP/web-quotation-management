from sqlalchemy import Column, Integer, String
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, composite


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    category: Mapped[str] = mapped_column(String(255), index=True)
    unit: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer())

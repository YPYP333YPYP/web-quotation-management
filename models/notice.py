from dataclasses import dataclass

from sqlalchemy import String, Text, Integer, DateTime, func
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column


@dataclass
class Notice(Base):
    __tablename__ = 'notices'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

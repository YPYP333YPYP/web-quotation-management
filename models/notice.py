from dataclasses import dataclass

from sqlalchemy import String, Text, Integer, DateTime, func
from core.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column


@dataclass
class Notice(Base):
    """공지사항을 관리하는 클래스

    Attributes:
        id (int): 고유한 공지사항 ID
        title (str): 공지사항 제목
        content (str): 공지사항 내용
        created_at (datetime): 공지사항 생성일 (자동 기록)
        updated_at (datetime): 공지사항 수정일 (수정된 경우 자동 갱신)
    """
    __tablename__ = 'notices'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

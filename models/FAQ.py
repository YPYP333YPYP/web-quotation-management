from dataclasses import dataclass

from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from core.db.database import Base


@dataclass
class FAQ(Base):
    """FAQ(자주 묻는 질문)를 관리하는 클래스

    Attributes:
        id (int): 고유한 FAQ ID
        category (str): FAQ 카테고리 (예: 계정, 결제 등)
        question (str): 질문 내용
        answer (str): 질문에 대한 답변
        created_at (datetime): FAQ 생성일 (자동 기록)
        updated_at (datetime): FAQ 수정일 (수정된 경우 자동 갱신)
    """
    __tablename__ = 'faqs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category: Mapped[str] = mapped_column(String(30), index=True)
    question: Mapped[str] = mapped_column(String(255), index=True)
    answer: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
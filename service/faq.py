from typing import Optional

from fastapi import Depends

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import GeneralException
from models.FAQ import FAQ
from repository.faq.faq import FAQRepository
from schemas.faq import FAQCreate


class FAQService:
    def __init__(self, faq_repository: FAQRepository = Depends(FAQRepository)):
        self.faq_repository = faq_repository

    async def create_faq(self, faq_data: FAQCreate):
        faq = FAQ(**faq_data.dict())
        await self.faq_repository.create_faq(faq)

    async def get_faq_by_id(self, faq_id: int) -> Optional[FAQ]:
        faq = await self.faq_repository.get_faq_by_id(faq_id)
        if not faq:
            raise GeneralException(ErrorStatus.FAQ_NOT_FOUND)
        return faq
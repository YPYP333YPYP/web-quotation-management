from typing import Optional

from fastapi import Depends

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import GeneralException
from models import FAQ
from repository.faq.faq import FAQRepository
from schemas.faq import FAQCreate, FAQUpdate


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

    async def get_all_faqs(self):
        return await self.faq_repository.get_all_faqs()

    async def update_faq(self, faq_id: int, faq_data: FAQUpdate):
        faq = await self.faq_repository.get_faq_by_id(faq_id)
        if not faq:
            raise GeneralException(ErrorStatus.FAQ_NOT_FOUND)
        await self.faq_repository.update_faq(faq_id, faq_data.dict())

    async def delete_faq(self, faq_id: int):
        faq = await self.faq_repository.get_faq_by_id(faq_id)
        if not faq:
            raise GeneralException(ErrorStatus.FAQ_NOT_FOUND)
        await self.faq_repository.delete_faq(faq_id)


from fastapi import Depends

from models.FAQ import FAQ
from repository.faq.faq import FAQRepository
from schemas.faq import FAQCreate


class FAQService:
    def __init__(self, faq_repository: FAQRepository = Depends(FAQRepository)):
        self.faq_repository = faq_repository

    async def create_faq(self, faq_data: FAQCreate):
        faq = FAQ(**faq_data.dict())
        await self.faq_repository.create_faq(faq)
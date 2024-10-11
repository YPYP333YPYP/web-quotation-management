from datetime import date, datetime
from typing import Sequence

from fastapi import Depends
from sqlalchemy import select, func, and_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from models import Quotation
from models.quotation_product import QuotationProduct
from schemas.quotation import QuotationStatus, QuotationUpdate


class QuotationRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    @handle_db_exceptions()
    async def create_quotation(self, quotation: Quotation):
        async with self.session as session:
            session.add(quotation)
            await session.commit()
            await session.refresh(quotation)
            return quotation

    @handle_db_exceptions()
    async def update_quotation(self, quotation_id: int, quotation_data: QuotationUpdate):
        async with self.session as session:
            async with session.begin():

                stmt = (
                    update(Quotation)
                    .where(Quotation.id == quotation_id)
                    .values(
                        client_id=quotation_data.client_id,
                        name=quotation_data.name,
                        total_price=quotation_data.total_price,
                        status=quotation_data.status,
                        particulars=quotation_data.particulars,
                        updated_at=func.now()
                    )
                )
                await session.execute(stmt)

                delete_stmt = delete(QuotationProduct).where(QuotationProduct.quotation_id == quotation_id)
                await session.execute(delete_stmt)

                for product in quotation_data.products:
                    quotation_product = QuotationProduct(
                        quotation_id=quotation_id,
                        product_id=product.id,
                        price=product.price,
                        quantity=product.quantity
                    )
                    session.add(quotation_product)

        async with self.session as session:
            result = await session.execute(select(Quotation).filter(Quotation.id == quotation_id))
            updated_quotation = result.scalar_one_or_none()
            return updated_quotation

    @handle_db_exceptions()
    async def get_quotation_by_id(self, quotation_id: int):
        async with self.session as session:
            product = await session.get(Quotation, quotation_id)
            return product if product else None

    @handle_db_exceptions()
    async def update_total_price(self, quotation_id: int) -> None:
        async with self.session as session:
            query = select(func.sum(QuotationProduct.price)). \
                where(QuotationProduct.quotation_id == quotation_id)
            result = await session.execute(query)
            total_price = result.scalar()

            query = select(Quotation).filter(Quotation.id == quotation_id)
            result = await session.execute(query)
            quotation = result.scalar_one_or_none()

            if quotation and total_price is not None:
                quotation.total_price = total_price
                quotation.updated_at = datetime.now()
                await session.commit()
            return total_price

    @handle_db_exceptions()
    async def search_quotation(self, start: date, end: date, query: str) -> Sequence[Quotation]:
        async with self.session as session:
            stmt = select(Quotation)

            if start:
                stmt = stmt.filter(Quotation.created_at >= start)
            if end:
                stmt = stmt.filter(Quotation.created_at <= end)
            if query:
                stmt = stmt.filter(Quotation.name.contains(query))

            tmp_result = await session.execute(stmt)
            result = tmp_result.scalars().all()

            return result

    @handle_db_exceptions()
    async def get_quotations_by_client_id(self, client_id: int, page: int = 1, page_size: int = 10):
        async with self.session as session:
            offset = (page - 1) * page_size

            count_query = select(func.count()).select_from(Quotation).where(Quotation.client_id == client_id)
            total = await session.scalar(count_query)

            query = (
                select(Quotation)
                .where(Quotation.client_id == client_id)
                .order_by(Quotation.created_at.desc())
                .offset(offset)
                .limit(page_size)
            )
            result = await session.execute(query)
            quotations = result.scalars().all()
            return quotations, total

    @handle_db_exceptions()
    async def get_quotations_by_data_range(self, client_id, start_date: date, end_date: date, page: int = 1,
                                           page_size: int = 10):
        async with self.session as session:
            count_query = (
                select(func.count())
                .select_from(Quotation)
                .where(and_(
                    Quotation.created_at.between(start_date, end_date),
                    Quotation.client_id == client_id
                ))
            )
            total = await session.scalar(count_query)

            offset = (page - 1) * page_size
            query = (
                select(Quotation)
                .where(and_(
                    Quotation.created_at.between(start_date, end_date),
                    Quotation.client_id == client_id
                ))
                .order_by(Quotation.created_at.desc())
                .offset(offset)
                .limit(page_size)
            )
            result = await session.execute(query)
            quotations = result.scalars().all()

            return quotations, total

    @handle_db_exceptions()
    async def get_today_quotation_ids(self, today: date):
        async with self.session as session:
            query = (select(Quotation.id).filter(func.date(Quotation.created_at) == today))
            result = await session.execute(query)
            quotation_ids = result.scalars().all()
            return quotation_ids

    @handle_db_exceptions()
    async def get_quotation_by_client_and_date(self, client_id: int, input_date: date):
        async with self.session as session:
            query = select(Quotation).where(
                and_(
                    Quotation.client_id == client_id,
                    func.date(Quotation.created_at) == input_date
                )
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @handle_db_exceptions()
    async def delete_quotation_product(self, quotation_id: int, product_id: int):
        async with self.session as session:
            query = select(QuotationProduct).where(
                and_(
                    QuotationProduct.quotation_id == quotation_id,
                    QuotationProduct.product_id == product_id
                )
            )
            result = await session.execute(query)
            quotation_product = result.scalar_one_or_none()

            if quotation_product:
                await session.delete(quotation_product)
                await session.commit()

    @handle_db_exceptions()
    async def exist_quotation_by_client_id_and_today_date(self, client_id: int, input_date: date) -> bool:
        async with self.session as session:
            query = select(Quotation).where(
                and_(
                    Quotation.client_id == client_id,
                    func.date(Quotation.input_date) == input_date
                )
            ).exists()

            result = await session.execute(select(query))
            quotation = result.scalar()
            return quotation

    @handle_db_exceptions()
    async def delete_quotation(self, quotation_id: int):
        async with self.session as session:
            quotation = await session.get(Quotation, quotation_id)
            await session.delete(quotation)
            await session.commit()

    @handle_db_exceptions()
    async def update_particulars(self, quotation_id, particulars):
        async with self.session as session:
            stmt = select(Quotation).filter(Quotation.id == quotation_id)
            result = await session.execute(stmt)
            quotation = result.scalar_one_or_none()

            quotation.particulars = particulars
            await session.commit()

    @handle_db_exceptions()
    async def update_status_completed(self, quotation_id):
        async with self.session as session:
            stmt = select(Quotation).filter(Quotation.id == quotation_id)
            result = await session.execute(stmt)
            quotation = result.scalar_one_or_none()

            quotation.status = QuotationStatus.COMPLETED.value
            await session.commit()

    @handle_db_exceptions()
    async def get_quotations_by_input_date(self, input_date):
        async with self.session as session:
            query = select(Quotation).filter(Quotation.input_date == input_date)

            result = await session.execute(query)
            return result.scalars().all()

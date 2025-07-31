from sqlalchemy import select
from src.models.library_model import BookModel
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional

class BookDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[BookModel]:
        result = await self.session.execute(select(BookModel))
        return result.scalars().all()

    async def get_by_id(self, book_id: UUID) -> Optional[BookModel]:
        result = await self.session.execute(select(BookModel).where(BookModel.id == book_id))
        return result.scalar_one_or_none()

    async def create(self, book_data: dict) -> BookModel:
        new_book = BookModel(**book_data)
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book
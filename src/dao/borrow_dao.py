from typing import Optional
from src.models.library_model import BorrowModel, BookModel
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date
from sqlalchemy import select

class BorrowDAO:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, borrow_data: dict) -> Optional[BorrowModel]:
        borrow = BorrowModel(**borrow_data)
        result = await self.session.execute(select(BookModel).where(BookModel.id == borrow.book_id))
        book = result.scalar_one_or_none()
        if book and book.quantity > 0:
            book.quantity -= 1
            borrow.status = "borrowed"
            self.session.add(borrow)
            await self.session.commit()
            await self.session.refresh(borrow)
            return borrow
        return None
    
    async def return_book(self, borrow_id: UUID) -> Optional[BorrowModel]:
        result = await self.session.execute(select(BorrowModel).where(BorrowModel.id == borrow_id))
        borrow = result.scalar_one_or_none()
        if not borrow or borrow.status != "borrowed":
            return None
        result = await self.session.execute(select(BookModel).where(BookModel.id == borrow.book_id))
        book = result.scalar_one_or_none()
        if book:
            book.quantity += 1
        borrow.return_date = date.today()
        borrow.status = "returned"
        await self.session.commit()
        await self.session.refresh(borrow)
        return borrow
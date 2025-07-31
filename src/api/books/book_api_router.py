from fastapi import APIRouter, HTTPException
from src.utils.db_utils import session_factory
from src.dto.book_dto import BookDTO
from src.dao.book_dao import BookDAO
from uuid import UUID

router = APIRouter()

@router.get("/books")
async def get_books():
    async with session_factory() as session:
        dao = BookDAO(session)
        books = await dao.get_all()
        return [book.__dict__ for book in books]

@router.get("/books/{book_id}")
async def get_book(book_id: UUID):
    async with session_factory() as session:
        dao = BookDAO(session)
        book = await dao.get_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book.__dict__

@router.post("/books")
async def add_book(book: BookDTO):
    async with session_factory() as session:
        dao = BookDAO(session)
        new_book = await dao.create(book.model_dump())
        return new_book.__dict__
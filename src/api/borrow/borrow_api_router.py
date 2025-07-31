from uuid import UUID
from fastapi import APIRouter, HTTPException
from src.utils.db_utils import session_factory
from src.dto.borrow_dto import BorrowDTO
from src.dao.borrow_dao import BorrowDAO

router = APIRouter()

@router.post("/rent")
async def rent_book(borrow: BorrowDTO):
    async with session_factory() as session:
        dao = BorrowDAO(session)
        result = await dao.create(borrow.model_dump())
        if not result:
            raise HTTPException(status_code=400, detail="Book not available")
        return result.__dict__

@router.post("/return")
async def return_book(borrow_id: UUID):
    async with session_factory() as session:
        dao = BorrowDAO(session)
        result = await dao.return_book(borrow_id)
        if not result:
            raise HTTPException(status_code=400, detail="Invalid borrow record")
        return result.__dict__
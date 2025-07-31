from uuid import UUID
from fastapi import APIRouter, HTTPException
from src.dao.user_dao import UserDAO
from src.dto.user_dto import UserDTO
from src.utils.db_utils import session_factory

router = APIRouter()

@router.get("/users")
async def get_users():
    async with session_factory() as session:
        dao = UserDAO(session)
        users = await dao.get_all()
        return [user.__dict__ for user in users]
    
@router.get("/users/{user_id}")
async def get_user(user_id: UUID):
    async with session_factory() as session:
        dao = UserDAO(session)
        user = await dao.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.__dict__
    
@router.post("/users")
async def add_user(user: UserDTO):
    async with session_factory() as session:
        dao = UserDAO(session)
        new_user = await dao.create(user.model_dump())
        return new_user.__dict__
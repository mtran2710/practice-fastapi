from typing import Optional, List
from src.models.library_model import UserModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

class UserDAO:
    def __init__(self, session: Session):
        self.session = session

    async def get_all(self) -> List[UserModel]:
        result = await self.session.execute(select(UserModel))
        return result.scalars().all()

    async def get_by_id(self, user_id: UUID) -> Optional[UserModel]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user_data: dict) -> UserModel:
        new_user = UserModel(**user_data)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
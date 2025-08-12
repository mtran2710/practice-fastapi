from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.models.todo_model import TodoModel

class TodoDAO:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self) -> List[TodoModel]:
        result = await self.session.execute(select(TodoModel))
        return result.scalars().all()
    
    async def get_by_id(self, todo_id: UUID) -> Optional[TodoModel]:
        result = await self.session.execute(select(TodoModel).where(TodoModel.id == todo_id))
        return result.scalar_one_or_none()
    
    async def create(self, todo_data: dict) -> TodoModel:
        now = datetime.now()
        todo_data["created_at"] = now
        todo_data["updated_at"] = now
        todo = TodoModel(**todo_data)
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        return todo
    
    async def update(self, todo_id: UUID, todo_data: dict) -> Optional[TodoModel]:
        todo = await self.get_by_id(todo_id)
        if not todo:
            return None 
        for key, value in todo_data.items():
            if key == "title" and value is None:
                continue
            setattr(todo, key, value)
        todo.updated_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(todo)
        return todo
    
    async def delete(self, todo_id: UUID) -> bool:
        todo = await self.get_by_id(todo_id)
        if not todo:
            return False
            
        await self.session.delete(todo)
        await self.session.commit()
        return True
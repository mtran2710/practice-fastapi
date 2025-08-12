from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db_utils import create_database_session
from src.dao.todo_dao import TodoDAO
from src.dto.todo_dto import (
    TodoUpdateRequest,
    TodoUpdateResponse,
    TodoCreateRequest
)

router = APIRouter()

def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None

@router.get("/todos")
async def get_todos(session: Annotated[AsyncSession, Depends(create_database_session)]):
    dao = TodoDAO(session)
    todos = await dao.get_all()
    result = []
    for todo in todos:
        todo_dict = todo.__dict__.copy()
        todo_dict["created_at"] = format_datetime(todo.created_at)
        todo_dict["updated_at"] = format_datetime(todo.updated_at)
        result.append(todo_dict)
    return result

@router.post("/todos")
async def create_todo(
    todo_data: TodoCreateRequest,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    dao = TodoDAO(session)
    new_todo = await dao.create(todo_data.model_dump())
    todo_dict = new_todo.__dict__.copy()
    todo_dict["created_at"] = format_datetime(new_todo.created_at)
    todo_dict["updated_at"] = format_datetime(new_todo.updated_at)
    return todo_dict

@router.put("/todos/{todo_id}", response_model=TodoUpdateResponse)
async def update_todo(
    todo_id: UUID,
    update_todo: TodoUpdateRequest,
    session: Annotated[AsyncSession, Depends(create_database_session)]
):
    if not update_todo.model_dump(exclude_unset=True):
        raise HTTPException(status_code=422, detail="Invalid update data")
    dao = TodoDAO(session)
    updated_todo = await dao.update(todo_id, update_todo.model_dump())
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_dict = updated_todo.__dict__.copy()
    todo_dict["updated_at"] = format_datetime(updated_todo.updated_at)
    return todo_dict

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: UUID, session: Annotated[AsyncSession, Depends(create_database_session)]):
    dao = TodoDAO(session)
    success = await dao.delete(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
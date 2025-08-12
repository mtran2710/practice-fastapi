from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class TodoCreateRequest(BaseModel):
    title: str
    completed: Optional[bool] = False

class TodoUpdateRequest(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = False

class TodoUpdateResponse(BaseModel):
    id: UUID
    title: str
    completed: bool
    updated_at: datetime
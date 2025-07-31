from pydantic import BaseModel
from uuid import UUID
from datetime import date

class BorrowDTO(BaseModel):
    user_id: UUID
    book_id: UUID
    due_date: date
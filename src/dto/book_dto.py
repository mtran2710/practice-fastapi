from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BookDTO(BaseModel):
    isbn: str
    title: str
    author_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    quantity: int
    published_year: Optional[int] = None
    publisher: Optional[str] = None
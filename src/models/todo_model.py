import uuid

from sqlalchemy import Boolean, Column, UUID, String, DateTime
from src.utils.db_utils import Base

class TodoModel(Base):
    __tablename__ = "todo_model"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
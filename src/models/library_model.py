import uuid
from sqlalchemy import Column, UUID, String, Integer, ForeignKey, Date

from src.utils.db_utils import Base

class UserModel(Base):
    __tablename__ = "user_model"

    id = Column(UUID, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<UserModel(id={self.id}, username={self.username}>"

class BookModel(Base):
    __tablename__ = "book_model"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    isbn = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("author_model.id", ondelete="SET NULL"), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("category_model.id", ondelete="SET NULL"), nullable=True)
    quantity = Column(Integer, nullable=False)
    published_year = Column(Integer, nullable=True)
    publisher = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<BookModel(id={self.id}, title={self.title}, author_id={self.author_id})>"

class AuthorModel(Base):
    __tablename__ = "author_model"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<AuthorModel(id={self.id}, name={self.name})>"
    
class CategoryModel(Base):
    __tablename__ = "category_model"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<CategoryModel(id={self.id}, name={self.name})>"
    
    
class BorrowModel(Base):
    __tablename__ = "borrow_model"    

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("book_model.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_model.id", ondelete="CASCADE"), nullable=False) 
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # "borrowed", "returned", "overdue"
    
    def __repr__(self):
        return f"<BorrowModel(id={self.id}, book_id={self.book_id}, user_id={self.user_id}, borrow_date={self.borrow_date}, due_date={self.due_date}, status={self.status})>"
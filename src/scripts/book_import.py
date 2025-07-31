import csv
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.models.library_model import BookModel, AuthorModel
from src.utils.db_utils import Base

# Update this with your actual database URL
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"
CSV_FILE_PATH = "test_data/books.csv"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_or_create_author(name):
    author = session.query(AuthorModel).filter_by(name=name).first()
    if not author:
        author = AuthorModel(id=uuid.uuid4(), name=name)
        session.add(author)
        session.commit()
    return author

def import_books(csv_path):
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            author = get_or_create_author(row["Book-Author"])
            book = BookModel(
                id=uuid.uuid4(),
                isbn=row["ISBN"],
                title=row["Book-Title"],
                author_id=author.id,
                quantity=1,
                published_year=int(row["Year-Of-Publication"]) if row["Year-Of-Publication"].isdigit() else None,
                publisher=row["Publisher"]
            )
            session.add(book)
        session.commit()

if __name__ == "__main__":
    # Create tables if not exist
    Base.metadata.create_all(engine)
    import_books(CSV_FILE_PATH)
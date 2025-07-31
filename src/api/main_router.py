from fastapi import APIRouter
from src.api.books.book_api_router import router as books_router
from src.api.users.user_api_router import router as users_router
from src.api.borrow.borrow_api_router import router as borrow_router

router = APIRouter()

router.include_router(books_router)
router.include_router(users_router)
router.include_router(borrow_router)

from fastapi import APIRouter
from src.api.hello_world.main import router as hello_world_router
from src.api.todo.main import router as to_do_router

router = APIRouter()

router.include_router(hello_world_router)
router.include_router(to_do_router, tags=["todo"])
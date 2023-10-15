from fastapi.routing import APIRouter

from ..api.books import router as books_router

api_router = APIRouter()

api_router.include_router(books_router, tags=["books"])

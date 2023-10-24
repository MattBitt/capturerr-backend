from fastapi.routing import APIRouter

from capturerrbackend.api.books import router as books_router
from capturerrbackend.api.captures import router as captures_router
from capturerrbackend.api.tags import router as tags_router
from capturerrbackend.api.users import router as users_router

api_router = APIRouter()

api_router.include_router(books_router, tags=["books"])
api_router.include_router(users_router, tags=["users"])
api_router.include_router(tags_router, tags=["tags"])
api_router.include_router(captures_router, tags=["captures"])

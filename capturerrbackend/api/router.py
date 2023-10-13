from fastapi.routing import APIRouter


from capturerrbackend.api.v1 import auth_router, users_router
from capturerrbackend.api.v2 import captures_router, tags_router, books_router


api_router = APIRouter()

api_router.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/v1/users", tags=["users"])

api_router.include_router(captures_router, tags=["capture"])
api_router.include_router(tags_router, tags=["tag"])
api_router.include_router(books_router, tags=["books"])

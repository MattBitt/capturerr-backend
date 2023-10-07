from .auth import router as auth_router
from .captures import router as captures_router
from .tags import router as tags_router
from .users import router as users_router

__all__ = ["captures_router", "tags_router", "auth_router", "users_router"]

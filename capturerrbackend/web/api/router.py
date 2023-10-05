from fastapi.routing import APIRouter

from capturerrbackend.web.api import bar, daz, dummy, echo, foo, monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(foo.router, prefix="/foo", tags=["foo"])
api_router.include_router(bar.router, prefix="/bar", tags=["bar"])
api_router.include_router(daz.router, prefix="/daz", tags=["daz"])

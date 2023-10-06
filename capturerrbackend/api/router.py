from fastapi.routing import APIRouter

from capturerrbackend.api import bar, daz, dummy, echo, foo, monitoring
from capturerrbackend.api.v1 import captures_router, tags_router

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(foo.router, prefix="/foo", tags=["foo"])
api_router.include_router(bar.router, prefix="/bar", tags=["bar"])
api_router.include_router(daz.router, prefix="/daz", tags=["daz"])
api_router.include_router(tags_router, prefix="/v1/capture", tags=["capture"])
api_router.include_router(captures_router, prefix="/v1/tag", tags=["tag"])
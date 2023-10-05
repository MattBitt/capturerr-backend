from fastapi.routing import APIRouter

from capturerrbackend.web.api import (
    bar,
    capture,
    daz,
    dummy,
    echo,
    foo,
    monitoring,
    tag,
    users,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(foo.router, prefix="/foo", tags=["foo"])
api_router.include_router(bar.router, prefix="/bar", tags=["bar"])
api_router.include_router(daz.router, prefix="/daz", tags=["daz"])
api_router.include_router(capture.router, prefix="/capture", tags=["capture"])
api_router.include_router(tag.router, prefix="/tag", tags=["tag"])

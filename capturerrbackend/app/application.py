from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from capturerrbackend.api.router import api_router
from capturerrbackend.app.lifetime import (
    register_shutdown_event,
    register_startup_event,
)
from capturerrbackend.app.logging import configure_logging
from capturerrbackend.app.middlewares import add_middleware


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="capturerrbackend",
        version=metadata.version("capturerrbackend"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    # Adds middlewares.
    _app = add_middleware(app)

    return _app

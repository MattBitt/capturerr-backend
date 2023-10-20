from importlib import metadata
from pprint import pprint
from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse, UJSONResponse
from loguru import logger

from capturerrbackend.app.presentation.app_exception_case import (
    AppExceptionCase,
    app_exception_handler,
)

from ..api.router import api_router
from ..app.infrastructure.sqlite.database import create_tables
from ..app.logging import configure_logging
from ..app.middlewares import add_middleware
from ..config.configurator import config


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    logger.warning("💥💥💥  Starting application ...💥💥💥")

    if "dev" in config.env:
        logger.debug("Creating tables")
        create_tables()
        pprint(config.model_dump())
        logger.critical(f"Environment: {config.env}")
        logger.info(f"Log Level: {config.log_level}")

    app = FastAPI(
        title="capturerr",
        version=metadata.version("capturerrbackend"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    @app.exception_handler(AppExceptionCase)
    async def custom_app_exception_handler(request: Any, e: Any) -> JSONResponse:
        return await app_exception_handler(request, e)

    # Adds startup and shutdown events.
    # register_startup_event(app)
    # register_shutdown_event(app)

    # Extend FastAPI default error handlers
    # app.exception_handler(RequestValidationError)(pydantic_validation_errors_handler)
    # app.exception_handler(BaseError)(custom_base_errors_handler)
    # app.exception_handler(ValidationError)(pydantic_validation_errors_handler)
    # app.exception_handler(Exception)(python_base_error_handler)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    # Adds middlewares.
    _app = add_middleware(app)

    return _app

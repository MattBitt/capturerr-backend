from contextlib import contextmanager
from pprint import pprint

from fastapi import FastAPI
from loguru import logger

from capturerrbackend.api.router import api_router
from capturerrbackend.app.infrastructure.sqlite.database import create_tables
from capturerrbackend.app.infrastructure.sqlite.database_async import sessionmanager
from capturerrbackend.app.logging import configure_logging
from capturerrbackend.app.middlewares import add_middleware
from capturerrbackend.config.configurator import config


def init_app(init_db=True) -> FastAPI:

    # if init_db:
    #     logger.debug("Creating tables from main app.  init_db was true")
    #     sessionmanager.init(config.db_url)

    #     @contextmanager
    #     def lifespan(app: FastAPI):
    #         logger.debug("life span begins here")
    #         yield
    #         if sessionmanager._engine is not None:
    #             sessionmanager.close()
    #         logger.debug("life span ends here")

    logger.debug("lifespan is not none🟡🟡🟡")

    app = FastAPI(
        title="capturerr",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    return app


def init_app_async(init_db=True) -> FastAPI:
    lifespan = None

    if init_db:
        sessionmanager.init(config.db_url)

        @contextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    app = FastAPI(
        title="capturerr",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    return app


def get_app(init_db=True) -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    logger.warning("💥💥💥  Starting application ...💥💥💥")

    if "prod" not in config.env:
        if init_db:
            logger.debug("Creating tables from main app.  init_db was true")
            create_tables()
            logger.debug("Tables created from main app")

    if "dev" in config.env:
        pprint(config.model_dump())
        logger.info(f"Environment: {config.env}")
        logger.info(f"Log Level: {config.log_level}")

    app = FastAPI(
        title="capturerr",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    # Adds middlewares.
    _app = add_middleware(app)
    logger.warning("💥💥💥  Finished setting up application ...💥💥💥")
    return _app

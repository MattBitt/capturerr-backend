from fastapi import FastAPI, Request, Response
from loguru import logger


def add_middleware(app: FastAPI) -> FastAPI:
    @app.middleware("http")
    async def api_logging(request: Request, call_next) -> Response:  # type: ignore
        response = await call_next(request)
        if "openapi.json" in request.url.path:
            return response
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        log_message = {
            "host": request.url.hostname,
            "endpoint": request.url.path,
            "response": response_body.decode(),
        }
        logger.debug(log_message)
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    return app

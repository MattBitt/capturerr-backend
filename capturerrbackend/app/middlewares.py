from fastapi import FastAPI


def add_middleware(app: FastAPI) -> FastAPI:
    # @app.middleware("http")
    # async def exception_handling(request: Request, call_next: Any) -> JSONResponse:
    #     try:
    #         return await call_next(request)
    #     except CustomException as e:
    #         return JSONResponse(
    #             status_code=e.status_code,
    #             content={
    #                 "error": "Client Error",
    #                 "detail": str(e.detail),
    #                 "status_code": str(e.status_code),
    #             },
    #         )
    #     except HTTPException as http_exception:
    #         return JSONResponse(
    #             status_code=http_exception.status_code,
    #             content={
    #                 "error": "Client Error",
    #                 "message": str(http_exception.detail),
    #             },
    #         )
    #     except Exception as e:
    #         message = f"{e.__class__.__name__} args: {e.args}"
    #         logger.error(message)
    #         return JSONResponse(
    #             status_code=500,
    #             content={
    #                 "error": "Internal Server Error",
    #                 "message": "An unexpected error occurred.",
    #             },
    #         )

    # @app.middleware("http")
    # async def api_logging(request: Request, call_next) -> Response:  # type: ignore
    #     try:
    #         response = await call_next(request)
    #     except Exception as e:
    #         logger.exception(e)
    #         raise e
    #     if "openapi.json" in request.url.path:
    #         return response
    #     response_body = b""
    #     async for chunk in response.body_iterator:
    #         response_body += chunk

    #     log_message = {
    #         "host": request.url.hostname,
    #         "endpoint": request.url.path,
    #         "response": response_body.decode(),
    #     }
    #     logger.debug(log_message)
    #     return Response(
    #         content=response_body,
    #         status_code=response.status_code,
    #         headers=dict(response.headers),
    #         media_type=response.media_type,
    #     )

    return app

from fastapi import FastAPI


def add_middleware(app: FastAPI) -> FastAPI:
    # 💥💥💥💥 Port these from an older version of the app.
    # @app.middleware("http")
    # async def add_version_header(request: Request, call_next) -> Response:
    #     logger.debug("Before Request")
    #     # logger.debug(request.content)
    #     # logger.debug(request.text)
    #     response = await call_next(request)
    #     logger.debug("After Request, preparing response")
    #     response.headers["X-Version"] = settings.VERSION
    #     return response

    # @app.middleware("http")
    # async def add_process_time_header(request: Request, call_next):
    #     start_time = time.time()
    #     response = await call_next(request)
    #     process_time = time.time() - start_time
    #     response.headers["X-Process-Time"] = f"{str(round(process_time*1000))}ms"
    #     return response

    return app

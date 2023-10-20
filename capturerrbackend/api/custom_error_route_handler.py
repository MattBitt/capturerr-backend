from collections import defaultdict
from functools import wraps
from typing import Any, Callable, Coroutine

from fastapi import HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from loguru import logger
from starlette.responses import JSONResponse

from capturerrbackend.app.domain.custom_exception import CustomException


class CustomErrorRouteHandler(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            if request.method == "GET" or request.method == "DELETE":
                request_payload = request.query_params
            else:
                request_payload = await request.json()

            logger.debug(f"Requested URL: {request.url}.")
            logger.debug(f"Payload: {request_payload} ")

            try:
                return await original_route_handler(request)

            except CustomException as err:
                logger.info(f"CustomException raised:  {err.detail}")
                return JSONResponse(
                    status_code=err.status_code,
                    content={
                        "error": "Client Error",
                        "detail": str(err.detail),
                        "status_code": str(err.status_code),
                    },
                )

            except RequestValidationError as exc:
                readable_error = await self.readable_errors_from_pydantic_message(exc)
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=jsonable_encoder(
                        {
                            "error": "Invalid Request",
                            "details": readable_error,
                            "status_code": 422,
                        },
                    ),
                )
            except Exception as err:
                logger.error(err)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return custom_route_handler

    async def readable_errors_from_pydantic_message(self, exc: Any) -> dict[Any, Any]:
        readable_error = defaultdict(list)
        for errors in exc.errors():
            loc, msg = errors["loc"], errors["msg"]
            filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
            field_string = ".".join(filtered_loc)
            readable_error[field_string].append(msg)
        return readable_error


# example usage:
# router = APIRouter(route_class=CustomErrorRouteHandler)


def my_error_handler(func: Any) -> Any:
    @wraps(func)
    def decorator(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)

        except CustomException as err:
            logger.info(err.detail)
            return JSONResponse(
                status_code=err.status_code,
                content={
                    "error": "Client Error",
                    "detail": str(err.detail),
                    "status_code": str(err.status_code),
                },
            )

        except Exception as err:
            logger.error(err)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return decorator

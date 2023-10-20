from typing import Any, Optional

from fastapi import Request
from fastapi.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: Optional[dict[Any, Any]]):
        self.exception_case: str = self.__class__.__name__
        self.status_code: int = status_code
        self.context: Optional[dict[Any, Any]] = context

    def __str__(self) -> str:
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(
    request: Request,
    exc: AppExceptionCase,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class AppException:
    class FooCreateItem(AppExceptionCase):
        def __init__(self, context: Optional[dict[Any, Any]]) -> None:
            """
            Item creation failed
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

    class FooGetItem(AppExceptionCase):
        def __init__(self, context: Optional[dict[Any, Any]]) -> None:
            """
            Item not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class FooItemRequiresAuth(AppExceptionCase):
        def __init__(self, context: Optional[dict[Any, Any]]) -> None:
            """
            Item is not public and requires auth
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, context)


if __name__ == "__main__":
    print([e for e in dir(AppException) if "__" not in e])

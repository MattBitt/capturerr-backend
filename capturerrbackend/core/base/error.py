from typing import Any

from starlette import status


class BaseError(Exception):
    def __init__(
        self,
        *_: tuple[Any],
        message: str = "",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        self.message: str = message
        self.status_code: int = status_code

        super().__init__(message)

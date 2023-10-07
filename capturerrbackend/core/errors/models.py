"""
most of this code was taken from this repo:

https://github.com/parfeniukink/medium_fastapi_layered_2023/

This module is responsible for describing shared errors

"""


from typing import Any

from starlette import status

from capturerrbackend.core.base.error import BaseError

__all__ = (
    "BaseError",
    "BadRequestError",
    "UnprocessableError",
    "NotFoundError",
    "DatabaseError",
    "AuthenticationError",
    "AuthorizationError",
)


class BadRequestError(BaseError):
    def __init__(self, *_: tuple[Any], message: str = "Bad request") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class UnprocessableError(BaseError):
    def __init__(self, *_: tuple[Any], message: str = "Validation error") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class NotFoundError(BaseError):
    def __init__(self, *_: tuple[Any], message: str = "Not found") -> None:
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class DatabaseError(BaseError):
    def __init__(self, *_: tuple[Any], message: str = "Database error") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class AuthenticationError(BaseError):
    def __init__(self, *_: tuple[Any], message: str = "Authentication error") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationError(BaseError):
    def __init__(self, *_: tuple[Any], message: str = "Authorization error") -> None:
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)

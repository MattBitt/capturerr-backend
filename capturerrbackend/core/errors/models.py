"""
most of this code was taken from this repo:

https://github.com/parfeniukink/medium_fastapi_layered_2023/

This module is responsible for describing shared errors

"""


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


class BadRequestError(BaseError):
    """
    _summary_

    Args:
        BaseError (_type_): _description_
    """

    def __init__(self, *_: tuple[Any], message: str = "Bad request") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class UnprocessableError(BaseError):
    """
    _summary_

    Args:
        BaseError (_type_): _description_
    """

    def __init__(self, *_: tuple[Any], message: str = "Validation error") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class NotFoundError(BaseError):
    """
    _summary_

    Args:
        BaseError (_type_): _description_
    """

    def __init__(self, *_: tuple[Any], message: str = "Not found") -> None:
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class DatabaseError(BaseError):
    """
    _summary_

    Args:
        BaseError (_type_): _description_
    """

    def __init__(self, *_: tuple[Any], message: str = "Database error") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class AuthenticationError(BaseError):
    """
    _summary_

    Args:
        BaseError (_type_): _description_
    """

    def __init__(self, *_: tuple[Any], message: str = "Authentication error") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationError(BaseError):
    """
    _summary_

    Args:
        BaseError (_type_): _description_
    """

    def __init__(self, *_: tuple[Any], message: str = "Authorization error") -> None:
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)

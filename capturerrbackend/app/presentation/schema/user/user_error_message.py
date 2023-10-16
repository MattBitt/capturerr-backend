from pydantic import BaseModel, Field

from capturerrbackend.app.domain.user.user_exception import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UsersNotFoundError,
)


class ErrorMessageUserNotFound(BaseModel):
    detail: str = Field(example=UserNotFoundError.message)


class ErrorMessageUsersNotFound(BaseModel):
    detail: str = Field(example=UsersNotFoundError.message)


class ErrorMessageUserAlreadyExists(BaseModel):
    detail: str = Field(example=UserAlreadyExistsError.message)

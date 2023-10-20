# from pydantic import BaseModel, Field


# from capturerrbackend.app.domain.user.user_exception import (
#     UserAlreadyExistsError,
#     UserBadCredentialsError,
#     UserNotFoundError,
#     UserNotSuperError,
#     UsersNotFoundError,
# )


# class ErrorMessageUserNotFound(BaseModel):
#     detail: str = Field(example=UserNotFoundError.message)


# class ErrorMessageUsersNotFound(BaseModel):
#     detail: str = Field(example=UsersNotFoundError.message)


# class ErrorMessageUserAlreadyExists(BaseModel):
#     detail: str = Field(example=UserAlreadyExistsError.message)


# class ErrorMessageBadCredentials(BaseModel):
#     detail: str = Field(example=UserBadCredentialsError.message)


# class ErrorMessageNotSuper(BaseModel):
#     detail: str = Field(example=UserNotSuperError.message)

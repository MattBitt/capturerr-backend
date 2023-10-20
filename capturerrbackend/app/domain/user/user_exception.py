# -*- coding: utf-8 -*-
"""User exception"""
from capturerrbackend.app.domain.custom_exception import CustomException


class UserNotFoundError(CustomException):
    """UserNotFoundError is an error that occurs when a user is not found."""

    status_code = 404
    detail = "The user you specified does not exist."

    def __str__(self) -> str:
        return UserNotFoundError.detail


class UsersNotFoundError(CustomException):
    """UsersNotFoundError is an error that occurs when users are not found."""

    status_code = 404
    detail = "No users were found."

    def __str__(self) -> str:
        return UsersNotFoundError.detail


class UserNameAlreadyExistsError(CustomException):
    """UserIsbnAlreadyExistsError is an error that occurs when a
    user with the same already exists."""

    status_code = 409
    detail = "The username you specified already exists."

    def __str__(self) -> str:
        return UserNameAlreadyExistsError.detail


class UserBadCredentialsError(CustomException):
    """UserBadCredentialsError is an error that occurs when a
    user cannot login with the credentials provided."""

    status_code = 401
    detail = "The credentials you specified do not match an existing account."

    def __str__(self) -> str:
        return UserBadCredentialsError.detail


class UserNotSuperError(CustomException):
    """UserNotSuperError is an error that occurs when a user is not an admin."""

    status_code = 409
    detail = "The user you specified does not have admin rights."

    def __str__(self) -> str:
        return UserNotSuperError.detail

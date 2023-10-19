# -*- coding: utf-8 -*-
"""User exception"""


class UserNotFoundError(Exception):
    """UserNotFoundError is an error that occurs when a user is not found."""

    message = "The user you specified does not exist."

    def __str__(self) -> str:
        return UserNotFoundError.message


class UsersNotFoundError(Exception):
    """UsersNotFoundError is an error that occurs when users are not found."""

    message = "No users were found."

    def __str__(self) -> str:
        return UsersNotFoundError.message


class UserAlreadyExistsError(Exception):
    """UserIsbnAlreadyExistsError is an error that occurs when a
    user with the same already exists."""

    message = "The user you specified already exists."

    def __str__(self) -> str:
        return UserAlreadyExistsError.message


class UserBadCredentialsError(Exception):
    """UserBadCredentialsError is an error that occurs when a
    user cannot login with the credentials provided."""

    message = "The credentials you specified do not match an existing account."

    def __str__(self) -> str:
        return UserBadCredentialsError.message


class UserNotSuperError(Exception):
    """UserNotSuperError is an error that occurs when a user is not an admin."""

    message = "The user you specified does not have admin rights."

    def __str__(self) -> str:
        return UserNotSuperError.message

# -*- coding: utf-8 -*-
"""User exception"""


class UserNotFoundError(Exception):
    """UserNotFoundError is an error that occurs when a user is not found."""

    message = "The user you spcecified does not exist."

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

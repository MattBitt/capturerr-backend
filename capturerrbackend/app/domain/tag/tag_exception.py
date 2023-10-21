# -*- coding: utf-8 -*-
"""Tag exception"""
from capturerrbackend.app.domain.custom_exception import CustomException


class TagNotFoundError(CustomException):
    """TagNotFoundError is an error that occurs when a tag is not found."""

    status_code = 404
    detail = "The tag you spcecified does not exist."

    def __str__(self) -> str:
        return TagNotFoundError.detail


class TagsNotFoundError(CustomException):
    """TagsNotFoundError is an error that occurs when tags are not found."""

    status_code = 404
    detail = "No tags were found."

    def __str__(self) -> str:
        return TagsNotFoundError.detail


class TagAlreadyExistsError(CustomException):
    """TagAlreadyExistsError is an error that occurs when a
    tag with the same name already exists."""

    status_code = 409
    detail = "A tag with the text you specified already exists."

    def __str__(self) -> str:
        return TagAlreadyExistsError.detail

# -*- coding: utf-8 -*-
"""Book exception"""
from capturerrbackend.app.domain.custom_exception import CustomException


class BookNotFoundError(CustomException):
    """BookNotFoundError is an error that occurs when a book is not found."""

    status_code = 404
    detail = "The book you spcecified does not exist."

    def __str__(self) -> str:
        return BookNotFoundError.detail


class BooksNotFoundError(CustomException):
    """BooksNotFoundError is an error that occurs when books are not found."""

    status_code = 404
    detail = "No books were found."

    def __str__(self) -> str:
        return BooksNotFoundError.detail


class BookIsbnAlreadyExistsError(CustomException):
    """BookIsbnAlreadyExistsError is an error that occurs when a
    book with the same ISBN code already exists."""

    status_code = 409
    detail = "The book with the ISBN code you specified already exists."

    def __str__(self) -> str:
        return BookIsbnAlreadyExistsError.detail

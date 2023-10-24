# -*- coding: utf-8 -*-
"""Capture exception"""
from capturerrbackend.app.domain.custom_exception import CustomException


class CaptureNotFoundError(CustomException):
    """CaptureNotFoundError is an error that occurs when a capture is not found."""

    status_code = 404
    detail = "The capture you spcecified does not exist."

    def __str__(self) -> str:
        return CaptureNotFoundError.detail


class CapturesNotFoundError(CustomException):
    """CapturesNotFoundError is an error that occurs when captures are not found."""

    status_code = 404
    detail = "No captures were found."

    def __str__(self) -> str:
        return CapturesNotFoundError.detail


class CaptureAlreadyExistsError(CustomException):
    """CaptureAlreadyExistsError is an error that occurs when a
    capture with the same ENTRY code already exists."""

    status_code = 409
    detail = "The capture with the ENTRY code you specified already exists."

    def __str__(self) -> str:
        return CaptureAlreadyExistsError.detail

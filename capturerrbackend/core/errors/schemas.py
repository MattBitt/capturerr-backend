# type ignore
from pydantic import Field, conlist

from capturerrbackend.core.base.schema import PublicModel

__all__ = (
    "ErrorResponse",
    "ErrorResponseMulti",
)


class ErrorResponse(PublicModel):
    """Error response model."""

    message: str = Field(description="This field represent the message")
    path: list = Field(  # type: ignore
        description="The path to the field that raised the error",
        default_factory=list,
    )


class ErrorResponseMulti(PublicModel):
    """The public error respnse model that includes multiple objects."""

    results: conlist(ErrorResponse, min_length=1)  # type: ignore

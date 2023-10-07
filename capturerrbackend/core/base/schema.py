from collections.abc import Mapping
from typing import Any, Generic

from capturerrbackend.core.base.model import PublicModel, _PublicModel

__all__ = (
    "ResponseMulti",
    "Response",
    "_Response",
)


class ResponseMulti(PublicModel, Generic[_PublicModel]):  # type: ignore
    """Generic response model that consist multiple results."""

    result: list[_PublicModel]


class Response(PublicModel, Generic[_PublicModel]):  # type: ignore
    """Generic response model that consist only one result."""

    result: _PublicModel


_Response = Mapping[int | str, dict[str, Any]]

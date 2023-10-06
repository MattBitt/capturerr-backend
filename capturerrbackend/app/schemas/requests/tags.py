from pydantic import BaseModel


class TagRequest(BaseModel):
    """DTO for creating new tag model."""

    title: str

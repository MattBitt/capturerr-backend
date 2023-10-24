from pydantic import BaseModel, Field


class CaptureCreateModel(BaseModel):
    """CaptureCreateModel represents a write model to create a capture."""

    entry: str = Field(example="Just ate a cheeseburger.")
    entry_type: str = Field(example="Food journal entry")
    notes: str = Field(
        example="It was delicious!.",
    )
    location: str = Field(example="McDonalds")
    flagged: bool = Field(example=False)
    priority: str = Field(example="low")
    happened_at: int = Field(example=1620000000)
    due_date: int = Field(example=1620000000)
    user_id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")


class CaptureUpdateModel(BaseModel):
    """CaptureUpdateModel represents a write model to update a capture."""

    entry: str = Field(example="Just ate a cheeseburger.")
    entry_type: str = Field(example="Food journal entry")
    notes: str = Field(
        example="It was delicious!.",
    )
    location: str = Field(example="McDonalds")
    flagged: bool = Field(example=False)
    priority: str = Field(example="low")
    happened_at: int = Field(example=1620000000)
    due_date: int = Field(example=1620000000)
    user_id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")

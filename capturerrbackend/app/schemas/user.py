from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    is_superuser: bool | None = None


class UserInDB(User):
    pk: int
    hashed_password: str = ""
    # created_at: datetime
    # updated_at: datetime


class UserRequest(User):
    password: str
    disabled: bool = False
    is_superuser: bool = False


class UserResponse(UserInDB):
    disabled: bool
    is_superuser: bool

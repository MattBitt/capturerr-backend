from typing import Annotated

from fastapi import APIRouter, Depends

from capturerrbackend.app.dao.users import UserRepo
from capturerrbackend.app.schemas.user import UserRequest, UserResponse
from capturerrbackend.app.services.users import get_current_active_user

router = APIRouter()

user_repo = UserRepo()


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[UserRequest, Depends(get_current_active_user)],
) -> UserResponse:
    return UserResponse.model_validate(current_user)


# @router.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[UserRequest, Depends(get_current_active_user)],
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]

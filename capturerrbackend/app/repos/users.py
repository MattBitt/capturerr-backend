from typing import Optional

from capturerrbackend.app.schemas.user import UserInDB, UserRequest, UserResponse
from capturerrbackend.core.db.users_db import users_db


class UserRepo:
    def create_new_user(self, user_data: UserRequest) -> UserResponse:
        user = UserInDB(**user_data.model_dump())
        user.id = len(users_db) + 1
        users_db.append(user.model_dump())
        return UserResponse.model_validate(user)

    # def get_user_by_email(self, email: str) -> UserResponse:  # new
    #     for user in users_db:
    #         if email in user["email"]:
    #             return user
    #     return None

    def get_by_username(self, username: str) -> Optional[UserResponse]:
        for user in users_db:
            if username == user["username"]:
                return UserResponse.model_validate(user)
        return None

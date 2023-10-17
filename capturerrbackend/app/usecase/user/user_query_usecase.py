from abc import ABC, abstractmethod
from typing import List, Optional

from capturerrbackend.app.domain.user.user_exception import (
    UserBadCredentialsError,
    UserNotFoundError,
    UsersNotFoundError,
)

from .user_query_model import UserLoginModel, UserReadModel
from .user_query_service import UserQueryService


def myhash(password: str) -> str:
    return "asdf" + password


class UserQueryUseCase(ABC):
    """UserQueryUseCase defines a query usecase inteface related User entity."""

    @abstractmethod
    def fetch_user_by_id(self, user_id: str) -> Optional[UserReadModel]:
        """fetch_user_by_id fetches a user by id."""
        raise NotImplementedError

    @abstractmethod
    def fetch_users(self) -> List[UserReadModel]:
        """fetch_users fetches users."""
        raise NotImplementedError

    @abstractmethod
    def fetch_user_by_user_name(self, user_name: str) -> Optional[UserReadModel]:
        """fetch_user_by_id fetches a user by id."""
        raise NotImplementedError

    @abstractmethod
    def login_user(self, data: UserLoginModel) -> Optional[UserReadModel]:
        """fetch_user_by_id fetches a user by id."""
        raise NotImplementedError


class UserQueryUseCaseImpl(UserQueryUseCase):
    """UserQueryUseCaseImpl implements a query usecases related User entity."""

    def __init__(self, user_query_service: UserQueryService):
        self.user_query_service: UserQueryService = user_query_service

    def fetch_user_by_id(self, user_id: str) -> Optional[UserReadModel]:
        """fetch_user_by_id fetches a user by id."""
        try:
            user = self.user_query_service.find_by_id(user_id)
            if user is None:
                raise UserNotFoundError
        except:
            raise

        return user

    def fetch_users(self) -> List[UserReadModel]:
        """fetch_users fetches users."""
        try:
            users = self.user_query_service.find_all()
            if users is None:
                raise UsersNotFoundError
        except:
            raise

        return users

    def fetch_user_by_user_name(self, user_name: str) -> Optional[UserReadModel]:
        """fetch_user_by_id fetches a user by id."""
        raise NotImplementedError

    def login_user(self, data: UserLoginModel) -> Optional[UserReadModel]:
        try:
            existing_user = self.user_query_service.find_by_user_name(data.user_name)
            if existing_user is None:
                raise UserNotFoundError

            new_password = myhash(data.password)
            if new_password != existing_user.hashed_password:
                raise UserBadCredentialsError

            user = self.user_query_service.find_by_user_name(data.user_name)
        except:
            raise

        return user

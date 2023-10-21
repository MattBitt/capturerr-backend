from abc import ABC, abstractmethod
from typing import List

from loguru import logger

from capturerrbackend.app.domain.user.user_exception import (
    UserBadCredentialsError,
    UserNotFoundError,
    UsersNotFoundError,
)

from .user_auth_service import verify_password
from .user_query_model import UserLoginModel, UserReadModel
from .user_query_service import UserQueryService


class UserQueryUseCase(ABC):
    """UserQueryUseCase defines a query usecase inteface related User entity."""

    @abstractmethod
    def fetch_user_by_id(self, user_id: str) -> UserReadModel:
        """fetch_user_by_id fetches a user by id."""
        raise NotImplementedError

    @abstractmethod
    def fetch_users(self) -> List[UserReadModel]:
        """fetch_users fetches users."""
        raise NotImplementedError

    @abstractmethod
    def fetch_user_by_user_name(self, user_name: str) -> UserReadModel:
        """fetch_user_by_id fetches a user by id."""
        raise NotImplementedError

    @abstractmethod
    def login_user(self, data: UserLoginModel) -> UserReadModel:
        """fetch_user_by_id fetches a user by id."""
        raise NotImplementedError


class UserQueryUseCaseImpl(UserQueryUseCase):
    """UserQueryUseCaseImpl implements a query usecases related User entity."""

    def __init__(self, user_query_service: UserQueryService):
        self.user_query_service: UserQueryService = user_query_service

    def fetch_user_by_id(self, user_id: str) -> UserReadModel:
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

    def fetch_user_by_user_name(self, user_name: str) -> UserReadModel:
        """fetch_user_by_user_name fetches a user by user_name"""
        try:
            user = self.user_query_service.find_by_user_name(user_name)
            if user is None:
                raise UserNotFoundError
        except:
            raise

        return user

    def login_user(self, data: UserLoginModel) -> UserReadModel:
        logger.debug("In login_user usecase")
        try:
            existing_user = self.user_query_service.find_by_user_name(data.user_name)
            if existing_user is None:
                raise UserNotFoundError
            if existing_user.hashed_password is None:
                raise UserBadCredentialsError
            if not verify_password(data.password, existing_user.hashed_password):
                raise UserBadCredentialsError

            user = self.user_query_service.find_by_user_name(data.user_name)
            if user is None:
                raise UserNotFoundError
        except:
            raise

        return user

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, cast
from uuid import uuid4

from loguru import logger

from capturerrbackend.app.domain.user.user import User
from capturerrbackend.app.domain.user.user_exception import (
    UserNameAlreadyExistsError,
    UserNotFoundError,
)
from capturerrbackend.app.domain.user.user_repository import UserRepository

from .user_auth_service import get_password_hash
from .user_command_model import UserCreateModel, UserUpdateModel
from .user_query_model import UserReadModel


def myhash(password: str) -> str:
    return "asdf" + password


class UserCommandUseCaseUnitOfWork(ABC):
    """UserCommandUseCaseUnitOfWork defines an interface based
    on Unit of Work pattern."""

    user_repository: UserRepository

    @abstractmethod
    def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class UserCommandUseCase(ABC):
    """UserCommandUseCase defines a command usecase inteface related User entity."""

    @abstractmethod
    def create_user(self, data: UserCreateModel) -> UserReadModel:
        raise NotImplementedError

    @abstractmethod
    def update_user(
        self,
        user_id: str,
        data: UserUpdateModel,
    ) -> Optional[UserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def delete_user_by_id(self, user_id: str) -> None:
        raise NotImplementedError


class UserCommandUseCaseImpl(UserCommandUseCase):
    """UserCommandUseCaseImpl implements a command usecases related User entity."""

    def __init__(
        self,
        uow: UserCommandUseCaseUnitOfWork,
    ):
        self.uow: UserCommandUseCaseUnitOfWork = uow

    def create_user(self, data: UserCreateModel) -> UserReadModel:
        try:
            uuid = uuid4().hex
            user = User(
                user_id=uuid,
                user_name=data.user_name,
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                is_superuser=data.is_superuser,
                hashed_password=get_password_hash(data.password),
                created_at=cast(int, datetime.now()),
                updated_at=cast(int, datetime.now()),
                deleted_at=None,
            )

            existing_user = self.uow.user_repository.find_by_user_name(user.user_name)
            if existing_user is not None:
                raise UserNameAlreadyExistsError

            self.uow.user_repository.create(user)
            self.uow.commit()

            created_user = self.uow.user_repository.find_by_id(uuid)
        except:
            self.uow.rollback()
            raise

        return UserReadModel.from_entity(cast(User, created_user))

    def update_user(
        self,
        user_id: str,
        data: UserUpdateModel,
    ) -> Optional[UserReadModel]:
        try:
            existing_user = self.uow.user_repository.find_by_id(user_id)
            if existing_user is None:
                raise UserNotFoundError

            user = User(
                user_id=user_id,
                user_name=data.user_name,
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                # updated_at=cast(int, datetime.now()),
            )

            self.uow.user_repository.update(user)

            updated_user = self.uow.user_repository.find_by_id(user.user_id)

            self.uow.commit()
        except Exception as err:
            logger.error(err)
            self.uow.rollback()
            raise

        return UserReadModel.from_entity(cast(User, updated_user))

    def delete_user_by_id(self, user_id: str) -> None:
        try:
            existing_user = self.uow.user_repository.find_by_id(user_id)
            if existing_user is None:
                raise UserNotFoundError

            self.uow.user_repository.delete_by_id(user_id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise

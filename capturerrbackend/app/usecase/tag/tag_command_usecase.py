from abc import ABC, abstractmethod
from typing import Optional, cast
from uuid import uuid4

from capturerrbackend.app.domain.tag.tag import Tag
from capturerrbackend.app.domain.tag.tag_exception import (
    TagAlreadyExistsError,
    TagNotFoundError,
)
from capturerrbackend.app.domain.tag.tag_repository import TagRepository

from .tag_command_model import TagCreateModel, TagUpdateModel
from .tag_query_model import TagReadModel


class TagCommandUseCaseUnitOfWork(ABC):
    """TagCommandUseCaseUnitOfWork defines an interface based
    on Unit of Work pattern."""

    tag_repository: TagRepository

    @abstractmethod
    def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class TagCommandUseCase(ABC):
    """TagCommandUseCase defines a command usecase inteface related Tag entity."""

    @abstractmethod
    def create_tag(self, data: TagCreateModel) -> TagReadModel:
        raise NotImplementedError

    @abstractmethod
    def get_or_create_tag(self, data: TagCreateModel) -> TagReadModel:
        raise NotImplementedError

    @abstractmethod
    def update_tag(
        self,
        tag_id: str,
        data: TagUpdateModel,
    ) -> Optional[TagReadModel]:
        raise NotImplementedError

    @abstractmethod
    def delete_tag_by_id(self, tag_id: str) -> None:
        raise NotImplementedError


class TagCommandUseCaseImpl(TagCommandUseCase):
    """TagCommandUseCaseImpl implements a command usecases related Tag entity."""

    def __init__(
        self,
        uow: TagCommandUseCaseUnitOfWork,
    ):
        self.uow: TagCommandUseCaseUnitOfWork = uow

    def create_tag(self, data: TagCreateModel) -> TagReadModel:
        try:
            uuid = uuid4().hex
            tag = Tag(
                id=uuid,
                text=data.text,
                user_id=data.user_id,
            )

            existing_tag = self.uow.tag_repository.find_by_text(data.text)
            if existing_tag is not None:
                raise TagAlreadyExistsError

            self.uow.tag_repository.create(tag)
            self.uow.commit()

            created_tag = self.uow.tag_repository.find_by_id(uuid)
            return TagReadModel.from_entity(cast(Tag, created_tag))
        except:
            self.uow.rollback()
            raise

    def get_or_create_tag(self, data: TagCreateModel) -> TagReadModel:
        try:
            existing_tag = self.uow.tag_repository.find_by_text(data.text)
            if existing_tag is not None:
                return TagReadModel.from_entity(existing_tag)
            uuid = uuid4().hex
            tag = Tag(
                id=uuid,
                text=data.text,
                user_id=data.user_id,
            )

            self.uow.tag_repository.create(tag)
            self.uow.commit()

            created_tag = self.uow.tag_repository.find_by_id(uuid)
            return TagReadModel.from_entity(cast(Tag, created_tag))
        except:
            self.uow.rollback()
            raise

    def update_tag(
        self,
        tag_id: str,
        data: TagUpdateModel,
    ) -> Optional[TagReadModel]:
        try:
            existing_tag = self.uow.tag_repository.find_by_id(tag_id)
            if existing_tag is None:
                raise TagNotFoundError

            tag = Tag(
                id=existing_tag.id,
                text=data.text,
                user_id=existing_tag.user_id,
            )

            self.uow.tag_repository.update(tag)

            updated_tag = self.uow.tag_repository.find_by_id(tag.id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return TagReadModel.from_entity(cast(Tag, updated_tag))

    def delete_tag_by_id(self, tag_id: str) -> None:
        try:
            existing_tag = self.uow.tag_repository.find_by_id(tag_id)
            if existing_tag is None:
                raise TagNotFoundError

            self.uow.tag_repository.delete_by_id(tag_id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise

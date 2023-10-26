from abc import ABC, abstractmethod
from typing import Optional, cast
from uuid import uuid4

from capturerrbackend.app.domain.capture.capture_repository import CaptureRepository

from ...domain.capture.capture import Capture
from ...domain.capture.capture_exception import (
    CaptureAlreadyExistsError,
    CaptureNotFoundError,
)
from .capture_command_model import CaptureCreateModel, CaptureUpdateModel
from .capture_query_model import CaptureReadModel


class CaptureCommandUseCaseUnitOfWork(ABC):
    """CaptureCommandUseCaseUnitOfWork defines an interface based
    on Unit of Work pattern."""

    capture_repository: CaptureRepository

    @abstractmethod
    def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class CaptureCommandUseCase(ABC):
    """CaptureCommandUseCase defines a command usecase inteface
    related Capture entity."""

    @abstractmethod
    def create_capture(self, data: CaptureCreateModel) -> CaptureReadModel:
        raise NotImplementedError

    @abstractmethod
    def update_capture(
        self,
        capture_id: str,
        data: CaptureUpdateModel,
    ) -> Optional[CaptureReadModel]:
        raise NotImplementedError

    @abstractmethod
    def delete_capture_by_id(self, capture_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_tag_to_capture(self, capture_id: str, tag_id: str) -> CaptureReadModel:
        raise NotImplementedError


class CaptureCommandUseCaseImpl(CaptureCommandUseCase):
    """CaptureCommandUseCaseImpl implements a command
    usecases related Capture entity."""

    def __init__(
        self,
        uow: CaptureCommandUseCaseUnitOfWork,
    ):
        self.uow: CaptureCommandUseCaseUnitOfWork = uow

    def create_capture(self, data: CaptureCreateModel) -> CaptureReadModel:
        try:
            uuid = uuid4().hex
            capture = Capture(
                capture_id=uuid,
                entry=data.entry,
                entry_type=data.entry_type,
                notes=data.notes,
                location=data.location,
                flagged=data.flagged,
                priority=data.priority,
                happened_at=data.happened_at,
                due_date=data.due_date,
                user_id=data.user_id,
            )

            existing_capture = self.uow.capture_repository.find_by_entry(data.entry)
            if existing_capture is not None:
                raise CaptureAlreadyExistsError

            self.uow.capture_repository.create(capture)
            self.uow.commit()

            created_capture = self.uow.capture_repository.find_by_id(uuid)
            return CaptureReadModel.from_entity(cast(Capture, created_capture))
        except:
            self.uow.rollback()
            raise

    def update_capture(
        self,
        capture_id: str,
        data: CaptureUpdateModel,
    ) -> Optional[CaptureReadModel]:
        try:
            existing_capture = self.uow.capture_repository.find_by_id(capture_id)
            if existing_capture is None:
                raise CaptureNotFoundError

            capture = Capture(
                capture_id=capture_id,
                user_id=data.user_id,
                entry=data.entry,
                entry_type=data.entry_type,
                notes=data.notes,
                location=data.location,
                flagged=data.flagged,
                priority=data.priority,
                happened_at=data.happened_at,
                due_date=data.due_date,
            )

            self.uow.capture_repository.update(capture)

            updated_capture = self.uow.capture_repository.find_by_id(capture.capture_id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return CaptureReadModel.from_entity(cast(Capture, updated_capture))

    def delete_capture_by_id(self, capture_id: str) -> None:
        try:
            existing_capture = self.uow.capture_repository.find_by_id(capture_id)
            if existing_capture is None:
                raise CaptureNotFoundError

            self.uow.capture_repository.delete_by_id(capture_id)
            self.uow.commit()
        except:
            self.uow.rollback()
            raise

    def add_tag_to_capture(self, capture_id: str, tag_id: str) -> CaptureReadModel:
        try:
            self.uow.capture_repository.add_tag(capture_id, tag_id)
            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        created_capture = self.uow.capture_repository.find_by_id(capture_id)
        return CaptureReadModel.from_entity(cast(Capture, created_capture))

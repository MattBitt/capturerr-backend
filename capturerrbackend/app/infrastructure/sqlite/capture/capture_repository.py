from typing import Optional

from sqlalchemy import insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from capturerrbackend.app.domain.capture.capture import Capture
from capturerrbackend.app.domain.capture.capture_repository import CaptureRepository
from capturerrbackend.app.infrastructure.sqlite.associations import capture_tags
from capturerrbackend.app.infrastructure.sqlite.capture.capture_dto import CaptureDTO
from capturerrbackend.app.usecase.capture import CaptureCommandUseCaseUnitOfWork


class CaptureRepositoryImpl(CaptureRepository):
    """CaptureRepositoryImpl implements CRUD operations related Capture
    entity using SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def find_by_id(self, capture_id: str) -> Optional[Capture]:
        try:
            capture_dto = self.session.query(CaptureDTO).filter_by(id=capture_id).one()
        except NoResultFound:
            return None
        except:
            raise

        return capture_dto.to_entity()

    def find_by_entry(self, entry: str) -> Optional[Capture]:
        try:
            capture_dto = self.session.query(CaptureDTO).filter_by(entry=entry).one()
        except NoResultFound:
            return None
        except:
            raise

        return capture_dto.to_entity()

    def create(self, capture: Capture) -> None:
        capture_dto = CaptureDTO.from_entity(capture)
        try:
            self.session.add(capture_dto)
        except:
            raise

    def update(self, capture: Capture) -> None:
        capture_dto = CaptureDTO.from_entity(capture)
        try:
            _capture = self.session.query(CaptureDTO).filter_by(id=capture_dto.id).one()
            _capture.entry = capture_dto.entry
            _capture.entry_type = capture_dto.entry_type
            _capture.notes = capture_dto.notes
            _capture.location = capture_dto.location
            _capture.priority = capture_dto.priority
            _capture.flagged = capture_dto.flagged
            _capture.updated_at = capture_dto.updated_at
        except:
            raise

    def delete_by_id(self, capture_id: str) -> None:
        try:
            self.session.query(CaptureDTO).filter_by(id=capture_id).delete()
        except:
            raise

    def add_tag(self, capture_id: str, tag_id: str) -> None:
        try:
            stmt = insert(capture_tags).values(capture_id=capture_id, tag_id=tag_id)
            self.session.execute(stmt)
        except:
            raise


class CaptureCommandUseCaseUnitOfWorkImpl(CaptureCommandUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        capture_repository: CaptureRepository,
    ):
        self.session: Session = session
        self.capture_repository: CaptureRepository = capture_repository

    def begin(self) -> None:
        self.session.begin()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

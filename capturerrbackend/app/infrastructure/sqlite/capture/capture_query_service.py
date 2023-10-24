from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from capturerrbackend.app.usecase.capture import CaptureQueryService, CaptureReadModel

from .capture_dto import CaptureDTO


class CaptureQueryServiceImpl(CaptureQueryService):
    """CaptureQueryServiceImpl implements READ operations
    related Capture entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[CaptureReadModel]:
        try:
            capture_dto = self.session.query(CaptureDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return capture_dto.to_read_model()

    def find_all(self) -> List[CaptureReadModel]:
        try:
            capture_dtos = (
                self.session.query(CaptureDTO)
                .order_by(CaptureDTO.updated_at)
                .limit(100)
                .all()
            )
        except:
            raise

        if len(capture_dtos) == 0:
            return []

        return list(map(lambda capture_dto: capture_dto.to_read_model(), capture_dtos))

    def find_by_user_id(self, user_id: str) -> List[CaptureReadModel]:
        try:
            capture_dtos = (
                self.session.query(CaptureDTO)
                .where(CaptureDTO.user_id == user_id)
                .order_by(CaptureDTO.updated_at)
                .limit(100)
                .all()
            )
        except:
            raise

        if len(capture_dtos) == 0:
            return []

        return list(map(lambda capture_dto: capture_dto.to_read_model(), capture_dtos))

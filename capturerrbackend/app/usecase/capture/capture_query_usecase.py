from abc import ABC, abstractmethod
from typing import List

from ...domain.capture.capture_exception import (
    CaptureNotFoundError,
    CapturesNotFoundError,
)
from .capture_query_model import CaptureReadModel
from .capture_query_service import CaptureQueryService


class CaptureQueryUseCase(ABC):
    """CaptureQueryUseCase defines a query usecase inteface related Capture entity."""

    @abstractmethod
    def fetch_capture_by_id(self, capture_id: str) -> CaptureReadModel:
        """fetch_capture_by_id fetches a capture by id."""
        raise NotImplementedError

    @abstractmethod
    def fetch_captures(self) -> List[CaptureReadModel]:
        """fetch_captures fetches captures."""
        raise NotImplementedError

    @abstractmethod
    def fetch_captures_for_user(self, user_id: str) -> List[CaptureReadModel]:
        """fetch_captures_by_user_id fetches captures by user id."""
        raise NotImplementedError


class CaptureQueryUseCaseImpl(CaptureQueryUseCase):
    """CaptureQueryUseCaseImpl implements a query usecases related Capture entity."""

    def __init__(self, capture_query_service: CaptureQueryService):
        self.capture_query_service: CaptureQueryService = capture_query_service

    def fetch_capture_by_id(self, capture_id: str) -> CaptureReadModel:
        """fetch_capture_by_id fetches a capture by id."""
        try:
            capture = self.capture_query_service.find_by_id(capture_id)
            if capture is None:
                raise CaptureNotFoundError
        except:
            raise

        return capture

    def fetch_captures(self) -> List[CaptureReadModel]:
        """fetch_captures fetches captures."""
        try:
            captures = self.capture_query_service.find_all()
            if captures is None or captures == []:
                raise CapturesNotFoundError
        except:
            raise

        return captures

    def fetch_captures_for_user(self, user_id: str) -> List[CaptureReadModel]:
        """fetch_captures_by_user_id fetches captures by user id."""
        try:
            captures = self.capture_query_service.find_by_user_id(user_id)
            if captures is None or captures == []:
                raise CapturesNotFoundError
        except:
            raise

        return captures

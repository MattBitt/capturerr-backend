from abc import ABC, abstractmethod
from typing import List, Optional

from .capture_query_model import CaptureReadModel


class CaptureQueryService(ABC):
    """CaptureQueryService defines a query service inteface related Capture entity."""

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[CaptureReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[CaptureReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[CaptureReadModel]:
        raise NotImplementedError

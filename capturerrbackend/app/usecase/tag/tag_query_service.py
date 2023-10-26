from abc import ABC, abstractmethod
from typing import List, Optional

from .tag_query_model import TagReadModel


class TagQueryService(ABC):
    """TagQueryService defines a query service inteface related Tag entity."""

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[TagReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_by_text(self, text: str) -> Optional[TagReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[TagReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[TagReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_by_capture_id(self, capture_id: str) -> List[TagReadModel]:
        raise NotImplementedError

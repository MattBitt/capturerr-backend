from abc import ABC, abstractmethod
from typing import List, Optional

from .user_query_model import UserReadModel


class UserQueryService(ABC):
    """UserQueryService defines a query service inteface related User entity."""

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[UserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[UserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_by_user_name(self, user_name: str) -> Optional[UserReadModel]:
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.tag.tag_exception import TagNotFoundError, TagsNotFoundError
from .tag_query_model import TagReadModel
from .tag_query_service import TagQueryService


class TagQueryUseCase(ABC):
    """TagQueryUseCase defines a query usecase inteface related Tag entity."""

    @abstractmethod
    def fetch_tag_by_id(self, tag_id: str) -> Optional[TagReadModel]:
        """fetch_tag_by_id fetches a tag by id."""
        raise NotImplementedError

    @abstractmethod
    def fetch_tags(self) -> List[TagReadModel]:
        """fetch_tags fetches tags."""
        raise NotImplementedError

    @abstractmethod
    def fetch_tags_by_user_id(self, user_id: str) -> List[TagReadModel]:
        """fetch_tags_by_user_id fetches tags by user id."""
        raise NotImplementedError


class TagQueryUseCaseImpl(TagQueryUseCase):
    """TagQueryUseCaseImpl implements a query usecases related Tag entity."""

    def __init__(self, tag_query_service: TagQueryService):
        self.tag_query_service: TagQueryService = tag_query_service

    def fetch_tag_by_id(self, tag_id: str) -> Optional[TagReadModel]:
        """fetch_tag_by_id fetches a tag by id."""
        try:
            tag = self.tag_query_service.find_by_id(tag_id)
            if tag is None:
                raise TagNotFoundError
        except:
            raise

        return tag

    def fetch_tags(self) -> List[TagReadModel]:
        """fetch_tags fetches tags."""
        try:
            tags = self.tag_query_service.find_all()
            if not tags:
                raise TagsNotFoundError
        except:
            raise

        return tags

    def fetch_tags_by_user_id(self, user_id: str) -> List[TagReadModel]:
        """fetch_tags_by_user_id fetches tags by user id."""
        try:
            tags = self.tag_query_service.find_by_user_id(user_id)
            if tags is None:
                raise TagsNotFoundError
        except:
            raise

        return tags

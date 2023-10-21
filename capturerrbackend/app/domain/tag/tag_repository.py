# -*- coding: utf-8 -*-
"""Tag repository"""

from abc import ABC, abstractmethod
from typing import Optional

from .tag import Tag


class TagRepository(ABC):
    """TagRepository defines a repository interface for Tag entity."""

    @abstractmethod
    def create(self, tag: Tag) -> Optional[Tag]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, tag_id: str) -> Optional[Tag]:
        raise NotImplementedError

    @abstractmethod
    def find_by_text(self, text: str) -> Optional[Tag]:
        raise NotImplementedError

    @abstractmethod
    def update(self, tag: Tag) -> Optional[Tag]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, tag_id: str) -> Optional[Tag]:
        raise NotImplementedError

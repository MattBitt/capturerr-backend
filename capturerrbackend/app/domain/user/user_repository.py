# -*- coding: utf-8 -*-
"""User repository"""

from abc import ABC, abstractmethod
from typing import Optional

from .user import User


class UserRepository(ABC):
    """UserRepository defines a repository interface for User entity."""

    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_user_name(self, user_name: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

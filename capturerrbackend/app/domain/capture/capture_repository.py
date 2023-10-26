# -*- coding: utf-8 -*-
"""Capture repository"""

from abc import ABC, abstractmethod
from typing import Optional

from .capture import Capture


class CaptureRepository(ABC):
    """CaptureRepository defines a repository interface for Capture entity."""

    @abstractmethod
    def create(self, capture: Capture) -> Optional[Capture]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, capture_id: str) -> Optional[Capture]:
        raise NotImplementedError

    @abstractmethod
    def find_by_entry(self, entry: str) -> Optional[Capture]:
        raise NotImplementedError

    @abstractmethod
    def update(self, capture: Capture) -> Optional[Capture]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, capture_id: str) -> Optional[Capture]:
        raise NotImplementedError

    @abstractmethod
    def add_tag(self, capture_id: str, tag_id: str) -> None:
        raise NotImplementedError

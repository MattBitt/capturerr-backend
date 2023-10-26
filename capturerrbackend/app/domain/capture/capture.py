# -*- coding: utf-8 -*-
"""Capture domain"""

from typing import Any, Optional


class Capture:
    """Capture represents your collection of captures as an entity."""

    def __init__(
        self,
        capture_id: str,
        user_id: str,
        entry: str,
        entry_type: str = "",  # should be enum
        notes: str = "",
        location: str = "",  # needs to be a location object
        flagged: bool = False,
        priority: str = "",  # should be enum
        happened_at: Optional[int] = None,
        due_date: Optional[int] = None,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
        deleted_at: Optional[int] = None,
        tags: Optional[list[Any]] = [],
    ):
        self.capture_id: str = capture_id
        self.user_id: str = user_id
        self.entry: str = entry
        self.entry_type: str = entry_type  # should be enu= entry_type
        self.notes: str = notes
        self.location: str = location
        self.flagged: bool = flagged
        self.priority: str = priority
        self.tags: Optional[list[Any]] = tags
        self.happened_at: Optional[int] = happened_at
        self.due_date: Optional[int] = due_date
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at
        self.deleted_at: Optional[int] = deleted_at

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Capture):
            return self.capture_id == obj.capture_id

        return False

# -*- coding: utf-8 -*-
"""Tag domain"""
from typing import Optional


class Tag:
    """Tag represents your collection of tags as an entity."""

    def __init__(
        self,
        id: str,
        text: str,
        user_id: str,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: str = id
        self.text: str = text
        self.user_id: str = user_id

        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Tag):
            return self.id == obj.id

        return False

# -*- coding: utf-8 -*-
"""Tag domain"""
from typing import Optional


class Tag:
    """Tag represents your collection of tags as an entity."""

    def __init__(
        self,
        tag_id: str,
        text: str,
        user_id: str,
        capture_id: str,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.tag_id: str = tag_id
        self.text: str = text
        self.user_id: str = user_id
        self.capture_id: str = capture_id
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Tag):
            return self.tag_id == obj.tag_id

        return False

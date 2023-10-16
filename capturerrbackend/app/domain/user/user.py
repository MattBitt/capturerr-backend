# -*- coding: utf-8 -*-
"""User domain"""

from typing import Optional


class User:
    """User represents your collection of users as an entity."""

    def __init__(
        self,
        user_id: str,
        user_name: str,
        first_name: str,
        last_name: str,
        email: str,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.user_id: str = user_id
        self.user_name: str = user_name
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def __eq__(self, obj: object) -> bool:
        # TODO where should this equality check be?
        if isinstance(obj, User):
            return self.user_id == obj.user_id

        return False

# -*- coding: utf-8 -*-
"""User domain"""

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from capturerrbackend.app.usecase.book.book_query_model import BookReadModel


class User:
    """User represents your collection of users as an entity."""

    def __init__(
        self,
        user_id: str,
        user_name: str,
        first_name: str,
        last_name: str,
        email: str,
        is_active: bool = True,
        is_superuser: bool = False,
        hashed_password: Optional[str] = None,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
        deleted_at: Optional[int] = None,
        books: List["BookReadModel"] = [],
    ):
        self.user_id: str = user_id
        self.user_name: str = user_name
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.is_active: bool = is_active
        self.is_superuser: bool = is_superuser
        self.hashed_password: Optional[str] = hashed_password
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at
        self.deleted_at: Optional[int] = deleted_at
        self.books: Optional[List["BookReadModel"]] = books

    def __eq__(self, obj: object) -> bool:
        # TODO where should this equality check be?
        if isinstance(obj, User):
            return self.user_id == obj.user_id

        return False

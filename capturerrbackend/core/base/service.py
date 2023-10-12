from typing import Any

from .repository import BaseRepo


class BaseService:
    def __init__(self, repository: BaseRepo) -> None:
        self._repository = repository

    def get_all(self) -> list[Any]:
        return self._repository.list()

    def get_list(self, schema: Any) -> None:
        # return self._repository.read_by_options(schema)
        raise NotImplementedError

    def get_by_id(self, id: int) -> Any:
        return self._repository.get(id)

    def add(self, schema):
        return self._repository.create(schema)

    def patch(self, id: int, schema: Any) -> None:
        # return self._repository.update(id, schema)
        raise NotImplementedError

    def patch_attr(self, id: int, attr: str, value: Any) -> None:
        # return self._repository.update_attr(id, attr, value)
        raise NotImplementedError

    def put_update(self, id: int, schema: Any) -> None:
        # return self._repository.whole_update(id, schema)
        raise NotImplementedError

    def remove_by_id(self, id: int) -> None:
        raise NotImplementedError

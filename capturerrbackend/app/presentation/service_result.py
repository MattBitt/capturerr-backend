from typing import Any

from .app_exception_case import AppExceptionCase


class ServiceResult:
    def __init__(self, arg: AppExceptionCase) -> None:
        if isinstance(arg, AppExceptionCase):
            self.success: bool = False
            self.exception_case = arg.exception_case
            self.status_code = arg.status_code
        else:
            self.success = True
            self.exception_case = "No exception_case"
            self.status_code = 0
        self.value = arg

    def __str__(self) -> str:
        if self.success:
            return "[Success]"
        else:
            return f'[Exception] "{self.exception_case}"'

    def __repr__(self) -> str:
        if self.success:
            return "<ServiceResult Success>"
        else:
            return f"<ServiceResult AppException {self.exception_case}>"

    def __enter__(self) -> Any:
        return self.value

    def __exit__(self, *kwargs: Any) -> None:
        pass


def handle_result(result: Any) -> Any:
    if not result.success:
        with result as exception:
            raise exception
    with result as result:
        return result

class CustomException(Exception):
    """CustomException base exception class"""

    status_code = 500
    detail = "An error occurred."

    def __str__(self) -> str:
        return CustomException.detail

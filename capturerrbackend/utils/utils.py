from datetime import datetime


def get_int_timestamp(dt: datetime) -> int:
    return int(dt.timestamp())

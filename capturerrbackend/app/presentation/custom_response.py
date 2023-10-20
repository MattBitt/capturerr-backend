import json
from typing import Any

from fastapi.responses import Response


class CustomResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        if content is None:
            return b""
        return json.dumps(content, ensure_ascii=False, indent=2).encode("utf-8")

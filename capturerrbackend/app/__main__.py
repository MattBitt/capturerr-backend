import uvicorn

from capturerrbackend.app.settings import settings

# TODO Does this file need to be here?
# Can't we just run uvicorn from the root directory?


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "capturerrbackend.app.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()

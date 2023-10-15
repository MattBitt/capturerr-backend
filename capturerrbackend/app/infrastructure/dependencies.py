from loguru import logger
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from ...config.configurator import config


def get_sync_session():  # type: ignore
    engine = create_engine(str(config.db_url), echo=config.db_echo)
    factory = sessionmaker(engine)
    with factory() as session:
        try:
            yield session
            session.commit()
        except exc.SQLAlchemyError as error:
            session.rollback()
            logger.error(error)
            raise


# def book_query_usecase(
#     session: Session = get_sync_session(),
# ) -> BookQueryUseCase:
#     """Get a book query use case."""
#     book_query_service: BookQueryService = BookQueryServiceImpl(session)
#     return BookQueryUseCaseImpl(book_query_service)


# def book_command_usecase(
#     session: Session,
# ) -> BookCommandUseCase:
#     """Get a book command use case."""
#     book_repository: BookRepository = BookRepositoryImpl(session)
#     uow: BookCommandUseCaseUnitOfWork = BookCommandUseCaseUnitOfWorkImpl(
#         session,
#         book_repository=book_repository,
#     )
#     return BookCommandUseCaseImpl(uow)

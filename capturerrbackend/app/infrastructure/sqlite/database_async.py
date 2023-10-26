# import contextlib
# from typing import AsyncIterator, Iterator

# from sqlalchemy import create_engine
# from sqlalchemy.engine import Connection, Engine
# from sqlalchemy.ext.asyncio import (
#     AsyncConnection,
#     AsyncEngine,
#     AsyncSession,
#     async_sessionmaker,
#     create_async_engine,
# )
# from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy.orm.session import Session

# Base = declarative_base()


# class DatabaseSessionManagerAsync:
#     def __init__(self):
#         self._engine: AsyncEngine | None = None
#         self._sessionmaker: async_sessionmaker | None = None

#     def init(self, host: str):
#         self._engine = create_async_engine(host)
#         self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

#     async def close(self):
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")
#         await self._engine.dispose()
#         self._engine = None
#         self._sessionmaker = None

#     @contextlib.asynccontextmanager
#     async def connect(self) -> AsyncIterator[AsyncConnection]:
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         async with self._engine.begin() as connection:
#             try:
#                 yield connection
#             except Exception:
#                 await connection.rollback()
#                 raise

#     @contextlib.asynccontextmanager
#     async def session(self) -> AsyncIterator[AsyncSession]:
#         if self._sessionmaker is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         session = self._sessionmaker()
#         try:
#             yield session
#         except Exception:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()

#     async def create_all(self, connection: AsyncConnection):
#         await connection.run_sync(Base.metadata.create_all)

#     async def drop_all(self, connection: AsyncConnection):
#         await connection.run_sync(Base.metadata.drop_all)


# class DatabaseSessionManagerSync:
#     def __init__(self):
#         self._engine: Engine | None = None
#         self._sessionmaker: sessionmaker | None = None

#     def init(self, host: str):
#         self._engine = create_engine(host)
#         self._sessionmaker = sessionmaker(autocommit=False, bind=self._engine)

#     def close(self):
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")
#         self._engine.dispose()
#         self._engine = None
#         self._sessionmaker = None

#     @contextlib.contextmanager
#     def connect(self) -> Iterator[Connection]:
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         with self._engine.begin() as connection:
#             try:
#                 yield connection
#             except Exception:
#                 connection.rollback()
#                 raise

#     @contextlib.contextmanager
#     def session(self) -> Iterator[Session]:
#         if self._sessionmaker is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         session = self._sessionmaker()
#         try:
#             yield session
#         except Exception:
#             session.rollback()
#             raise
#         finally:
#             session.close()

#     def create_all(self, connection: Session):
#         connection.run_sync(Base.metadata.create_all)

#     def drop_all(self, connection: Session):
#         connection.run_sync(Base.metadata.drop_all)


# sessionmanager = DatabaseSessionManagerSync()
# sessionmanagerAsync = DatabaseSessionManagerAsync()


# def get_db():
#     with sessionmanager.session() as session:
#         yield session


# def get_db_async():
#     with sessionmanagerAsync.session() as session:
#         yield session

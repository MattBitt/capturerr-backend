from datetime import datetime
from typing import Optional, cast

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from capturerrbackend.app.domain.user.user import User
from capturerrbackend.app.domain.user.user_repository import UserRepository
from capturerrbackend.app.usecase.user import UserCommandUseCaseUnitOfWork

from .user_dto import UserDTO


class UserRepositoryImpl(UserRepository):
    """UserRepositoryImpl implements CRUD operations related User
    entity using SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def find_by_id(self, user_id: str) -> Optional[User]:
        try:
            user_dto = self.session.query(UserDTO).filter_by(id=user_id).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_dto.to_entity()

    def find_by_user_name(self, user_name: str) -> Optional[User]:
        try:
            user_dto = self.session.query(UserDTO).filter_by(user_name=user_name).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_dto.to_entity()

    def create(self, user: User) -> None:
        user_dto = UserDTO.from_entity(user)
        try:
            self.session.add(user_dto)
        except:
            raise

    def update(self, user: User) -> None:
        user_dto = UserDTO.from_entity(user)
        try:
            _user = self.session.query(UserDTO).filter_by(id=user_dto.id).one()
            _user.user_name = user_dto.user_name
            _user.first_name = user_dto.first_name
            _user.last_name = user_dto.last_name
            # _user.updated_at = user_dto.updated_at

        except:
            raise

    def delete_by_id(self, user_id: str) -> None:
        try:
            user_dto = self.session.query(UserDTO).filter_by(id=user_id).one()
            user_dto.is_active = False
            user_dto.deleted_at = cast(int, datetime.now())
        except:
            raise


class UserCommandUseCaseUnitOfWorkImpl(UserCommandUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        user_repository: UserRepository,
    ):
        self.session: Session = session
        self.user_repository: UserRepository = user_repository

    def begin(self) -> None:
        self.session.begin()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

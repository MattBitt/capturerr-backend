from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from capturerrbackend.app.usecase.user import UserQueryService, UserReadModel

from .user_dto import UserDTO


class UserQueryServiceImpl(UserQueryService):
    """UserQueryServiceImpl implements READ operations
    related User entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[UserReadModel]:
        try:
            user_dto = self.session.query(UserDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_dto.to_read_model()

    def find_all(self) -> List[UserReadModel]:
        try:
            user_dtos = (
                self.session.query(UserDTO)
                .order_by(UserDTO.updated_at)
                .limit(100)
                .all()
            )
        except:
            raise

        if len(user_dtos) == 0:
            return []

        return list(map(lambda user_dto: user_dto.to_read_model(), user_dtos))

    def find_by_user_name(self, user_name: str) -> Optional[UserReadModel]:
        try:
            user_dto = self.session.query(UserDTO).filter_by(user_name=user_name).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_dto.to_read_model()

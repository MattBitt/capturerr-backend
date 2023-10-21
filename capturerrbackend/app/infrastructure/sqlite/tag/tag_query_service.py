from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from ....usecase.tag import TagQueryService, TagReadModel
from .tag_dto import TagDTO


class TagQueryServiceImpl(TagQueryService):
    """TagQueryServiceImpl implements READ operations
    related Tag entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[TagReadModel]:
        try:
            tag_dto = self.session.query(TagDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return tag_dto.to_read_model()

    def find_all(self) -> List[TagReadModel]:
        try:
            tag_dtos = (
                self.session.query(TagDTO).order_by(TagDTO.updated_at).limit(100).all()
            )
        except:
            raise

        if len(tag_dtos) == 0:
            return []

        return list(map(lambda tag_dto: tag_dto.to_read_model(), tag_dtos))

    def find_by_user_id(self, user_id: str) -> List[TagReadModel]:
        try:
            tag_dtos = (
                self.session.query(TagDTO)
                .where(TagDTO.user_id == user_id)
                .order_by(TagDTO.updated_at)
                .limit(100)
                .all()
            )
        except:
            raise

        if len(tag_dtos) == 0:
            return []

        return list(map(lambda tag_dto: tag_dto.to_read_model(), tag_dtos))

    def find_by_text(self, text: str) -> Optional[TagReadModel]:
        try:
            tag_dto = self.session.query(TagDTO).filter_by(text=text).one()
        except NoResultFound:
            return None
        except:
            raise

        return tag_dto.to_read_model()

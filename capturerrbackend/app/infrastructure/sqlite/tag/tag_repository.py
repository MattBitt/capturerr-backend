from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from capturerrbackend.app.domain.tag.tag import Tag
from capturerrbackend.app.domain.tag.tag_repository import TagRepository
from capturerrbackend.app.usecase.tag import TagCommandUseCaseUnitOfWork

from .tag_dto import TagDTO


class TagRepositoryImpl(TagRepository):
    """TagRepositoryImpl implements CRUD operations related Tag
    entity using SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def find_by_id(self, tag_id: str) -> Optional[Tag]:
        try:
            tag_dto = self.session.query(TagDTO).filter_by(id=tag_id).one()
        except NoResultFound:
            return None
        except:
            raise

        return tag_dto.to_entity()

    def find_by_text(self, text: str) -> Optional[Tag]:
        try:
            tag_dto = self.session.query(TagDTO).filter_by(text=text).one()
        except NoResultFound:
            return None
        except:
            raise

        return tag_dto.to_entity()

    def create(self, tag: Tag) -> None:
        tag_dto = TagDTO.from_entity(tag)
        try:
            self.session.add(tag_dto)
        except:
            raise

    def update(self, tag: Tag) -> None:
        tag_dto = TagDTO.from_entity(tag)
        try:
            _tag = self.session.query(TagDTO).filter_by(id=tag_dto.id).one()
            _tag.text = tag_dto.text
            _tag.updated_at = tag_dto.updated_at
        except:
            raise

    def delete_by_id(self, tag_id: str) -> None:
        try:
            self.session.query(TagDTO).filter_by(id=tag_id).delete()
        except:
            raise


class TagCommandUseCaseUnitOfWorkImpl(TagCommandUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        tag_repository: TagRepository,
    ):
        self.session: Session = session
        self.tag_repository: TagRepository = tag_repository

    def begin(self) -> None:
        self.session.begin()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

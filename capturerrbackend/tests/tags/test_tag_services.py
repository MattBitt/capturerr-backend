from sqlalchemy.orm import Session

from capturerrbackend.app.infrastructure.sqlite.tag import TagQueryServiceImpl
from capturerrbackend.app.usecase.capture import CaptureReadModel

# from ..app.infrastructure.dependencies import tag_command_usecase, tag_query_usecase
from capturerrbackend.app.usecase.tag import TagCreateModel, TagQueryService


def test_tag_query_service_find(
    db_fixture: Session,
    new_tag_in_db: TagCreateModel,
    new_capture_in_db: CaptureReadModel,
) -> None:
    tag_query_service: TagQueryService = TagQueryServiceImpl(db_fixture)
    assert isinstance(tag_query_service, TagQueryServiceImpl)

    new_tag = tag_query_service.find_by_text(new_tag_in_db.text)
    assert new_tag is not None
    assert new_tag.text == new_tag_in_db.text

    _id = new_tag.id
    new_tag2 = tag_query_service.find_by_id(_id)
    assert new_tag2 is not None
    assert new_tag2 == new_tag

    _user_id = new_tag.user_id
    new_tag3 = tag_query_service.find_by_user_id(_user_id)
    assert len(new_tag3) == 1
    assert new_tag3[0] == new_tag

    # _capture_id = new_capture_in_db.id

    # new_tag4 = tag_query_service.find_by_capture_id(_capture_id)
    # assert len(new_tag4) == 1
    # assert new_tag4[0] == new_tag

    tags = tag_query_service.find_all()
    assert len(tags) == 1
    assert tags[0] == new_tag_in_db

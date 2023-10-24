from sqlalchemy.orm import Session

from capturerrbackend.app.infrastructure.sqlite.capture import CaptureQueryServiceImpl

# from ..app.infrastructure.dependencies import capture_command_usecase, capture_query_usecase
from capturerrbackend.app.usecase.capture import CaptureCreateModel, CaptureQueryService


def test_capture_query_service_find(
    db_fixture: Session,
    new_capture_in_db: CaptureCreateModel,
) -> None:
    capture_query_service: CaptureQueryService = CaptureQueryServiceImpl(db_fixture)
    assert isinstance(capture_query_service, CaptureQueryServiceImpl)

    new_capture = capture_query_service.find_by_id(new_capture_in_db.id)
    assert new_capture is not None
    assert new_capture.id == new_capture_in_db.id

    _user_id = new_capture.user_id
    new_capture2 = capture_query_service.find_by_user_id(_user_id)
    assert new_capture2 is not None
    assert new_capture2[0] == new_capture

    captures = capture_query_service.find_all()
    assert len(captures) == 1
    assert captures[0] == new_capture_in_db

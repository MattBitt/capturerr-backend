from datetime import datetime
from typing import Any

from capturerrbackend.app.domain.capture.capture_exception import (
    CaptureAlreadyExistsError,
    CaptureNotFoundError,
    CapturesNotFoundError,
)
from capturerrbackend.app.usecase.capture import (
    CaptureCommandUseCaseImpl,
    CaptureCreateModel,
    CaptureQueryUseCaseImpl,
    CaptureReadModel,
    CaptureUpdateModel,
)
from capturerrbackend.app.usecase.tag import (
    TagCommandUseCaseImpl,
    TagCreateModel,
    TagQueryUseCaseImpl,
)
from capturerrbackend.app.usecase.user import UserReadModel
from capturerrbackend.utils.utils import get_int_timestamp


def test_create_capture(
    fake_capture: dict[str, Any],
    capture_command_usecase: CaptureCommandUseCaseImpl,
    capture_query_usecase: CaptureQueryUseCaseImpl,
) -> None:
    # Arrange

    capture_model = CaptureCreateModel.model_validate(fake_capture)
    capture = capture_command_usecase.create_capture(
        capture_model,
    )
    assert capture is not None

    all_captures = capture_query_usecase.fetch_captures()
    assert len(all_captures) > 0
    assert all_captures[0].entry == fake_capture["entry"]


def test_create_capture_duplicate_entry(
    fake_capture: dict[str, Any],
    capture_command_usecase: CaptureCommandUseCaseImpl,
    capture_query_usecase: CaptureQueryUseCaseImpl,
) -> None:
    # Arrange

    capture_model = CaptureCreateModel.model_validate(fake_capture)
    capture = capture_command_usecase.create_capture(
        capture_model,
    )
    assert capture is not None
    try:
        # add the same capture again
        capture_command_usecase.create_capture(
            capture_model,
        )
        assert True is False
    except CaptureAlreadyExistsError as e:
        assert e.detail == CaptureAlreadyExistsError.detail
    except:
        assert True is False
        raise


def test_get_capture(
    fake_capture: dict[str, Any],
    capture_command_usecase: CaptureCommandUseCaseImpl,
    capture_query_usecase: CaptureQueryUseCaseImpl,
) -> None:
    # Arrange

    capture_model = CaptureCreateModel.model_validate(fake_capture)
    capture = capture_command_usecase.create_capture(
        capture_model,
    )
    assert capture is not None

    capture2 = capture_query_usecase.fetch_capture_by_id(capture.id)
    assert capture2 is not None
    assert capture2.entry == fake_capture["entry"]


def test_get_capture_for_user(
    fake_capture: dict[str, Any],
    new_user_in_db: UserReadModel,
    new_super_user_in_db: UserReadModel,
    capture_command_usecase: CaptureCommandUseCaseImpl,
    capture_query_usecase: CaptureQueryUseCaseImpl,
) -> None:
    # Arrange
    fake_capture["user_id"] = new_user_in_db.id
    initial_entry = fake_capture["entry"]
    # create first capture

    capture_model = CaptureCreateModel.model_validate(fake_capture)
    capture = capture_command_usecase.create_capture(
        capture_model,
    )
    assert capture is not None

    # create first capture
    fake_capture["entry"] = "new entry"
    capture_model = CaptureCreateModel.model_validate(fake_capture)
    capture = capture_command_usecase.create_capture(
        capture_model,
    )
    assert capture is not None

    # create 3rd capture
    fake_capture["entry"] = "another new entry.  this time from the admin"
    fake_capture["user_id"] = new_super_user_in_db.id
    capture_model = CaptureCreateModel.model_validate(fake_capture)
    capture = capture_command_usecase.create_capture(
        capture_model,
    )

    my_caps = capture_query_usecase.fetch_captures_for_user(new_user_in_db.id)
    assert len(my_caps) == 2
    assert my_caps[0].entry == initial_entry


def test_get_capture_no_captures(
    capture_command_usecase: CaptureCommandUseCaseImpl,
    capture_query_usecase: CaptureQueryUseCaseImpl,
) -> None:
    # Arrange
    try:
        capture_query_usecase.fetch_captures()
        assert False
    except CapturesNotFoundError as e:
        assert e.status_code == CapturesNotFoundError.status_code
        assert e.detail == CapturesNotFoundError.detail


def test_update_capture_bad_id(
    fake_capture: dict[str, Any],
    capture_command_usecase: CaptureCommandUseCaseImpl,
    capture_query_usecase: CaptureQueryUseCaseImpl,
) -> None:
    # Arrange

    capture_model = CaptureCreateModel.model_validate(fake_capture)
    capture = capture_command_usecase.create_capture(
        capture_model,
    )
    assert capture is not None
    capture.entry_type = "updated entry type"
    updated_capture = CaptureUpdateModel.model_validate(capture.model_dump())

    try:
        capture_command_usecase.update_capture("bad_id", updated_capture)
        assert False
    except CaptureNotFoundError as e:
        assert e.status_code == CaptureNotFoundError.status_code
        assert e.detail == CaptureNotFoundError.detail


def test_add_new_tag_to_capture(
    new_capture_in_db: CaptureReadModel,
    capture_command_usecase: CaptureCommandUseCaseImpl,
    capture_query_usecase: CaptureQueryUseCaseImpl,
    tag_command_usecase: TagCommandUseCaseImpl,
    tag_query_usecase: TagQueryUseCaseImpl,
) -> None:
    # Arrange
    capture = new_capture_in_db

    tag_info = {
        "user_id": capture.user_id,
        "text": "a-brand-new-tag-that-doesnt-exist-yet15",
        "created_at": get_int_timestamp(datetime.now()),
        "updated_at": get_int_timestamp(datetime.now()),
    }
    tag_model = TagCreateModel.model_validate(tag_info)
    tag = tag_command_usecase.get_or_create_tag(tag_model)

    # new_tag = tag_command_usecase.create_tag(tag)

    # assert capture.tags is None
    # assert tag.captures is None
    capture_command_usecase.add_tag_to_capture(capture.id, tag.id)
    new_tag = tag_query_usecase.fetch_tag_by_text(tag.text)
    assert new_tag is not None
    capture.tags = tag_query_usecase.fetch_tags_for_capture(capture.id)

    # updated_capture = capture_query_usecase.fetch_capture_by_id(capture.id)
    # updated_tag = capture_query_usecase.fetch_tag_by_id(tag.id)
    # assert capture_tags.tags is not None
    # assert tag.captures is not None
    assert capture.tags[0].id is not None
    # assert tag.captures[0].id == capture.id

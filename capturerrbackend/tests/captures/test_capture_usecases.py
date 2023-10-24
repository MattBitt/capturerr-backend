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
    CaptureUpdateModel,
)
from capturerrbackend.app.usecase.user import UserReadModel


def test_create_capture(
    fake_capture: dict[str, Any],
    new_user_in_db: dict[str, Any],
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

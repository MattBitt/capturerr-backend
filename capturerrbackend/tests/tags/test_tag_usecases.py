from typing import Any

from capturerrbackend.app.domain.tag.tag_exception import (
    TagAlreadyExistsError,
    TagNotFoundError,
    TagsNotFoundError,
)
from capturerrbackend.app.usecase.tag import (
    TagCommandUseCaseImpl,
    TagCreateModel,
    TagQueryUseCaseImpl,
    TagUpdateModel,
)


def test_create_tag(
    fake_tag: dict[str, Any],
    tag_command_usecase: TagCommandUseCaseImpl,
    tag_query_usecase: TagQueryUseCaseImpl,
) -> None:
    # Arrange

    tag_model = TagCreateModel.model_validate(fake_tag)
    tag = tag_command_usecase.create_tag(
        tag_model,
    )
    assert tag is not None

    all_tags = tag_query_usecase.fetch_tags()
    assert len(all_tags) > 0
    assert all_tags[0].text == fake_tag["text"]


def test_create_tag_duplicate_text(
    fake_tag: dict[str, Any],
    tag_command_usecase: TagCommandUseCaseImpl,
    tag_query_usecase: TagQueryUseCaseImpl,
) -> None:
    # Arrange

    tag_model = TagCreateModel.model_validate(fake_tag)
    tag = tag_command_usecase.create_tag(
        tag_model,
    )
    assert tag is not None
    try:
        # add the same tag again
        tag_command_usecase.create_tag(
            tag_model,
        )
        assert True is False
    except TagAlreadyExistsError as e:
        assert e.detail == TagAlreadyExistsError.detail
    except:
        assert True is False
        raise


def test_get_tag(
    fake_tag: dict[str, Any],
    tag_command_usecase: TagCommandUseCaseImpl,
    tag_query_usecase: TagQueryUseCaseImpl,
) -> None:
    # Arrange

    tag_model = TagCreateModel.model_validate(fake_tag)
    tag = tag_command_usecase.create_tag(
        tag_model,
    )
    assert tag is not None

    tag2 = tag_query_usecase.fetch_tag_by_id(tag.id)
    assert tag2 is not None
    assert tag2.text == fake_tag["text"]


def test_get_tag_no_tags(
    tag_command_usecase: TagCommandUseCaseImpl,
    tag_query_usecase: TagQueryUseCaseImpl,
) -> None:
    # Arrange
    try:
        tag_query_usecase.fetch_tags()
        assert False
    except TagsNotFoundError as e:
        assert e.status_code == TagsNotFoundError.status_code
        assert e.detail == TagsNotFoundError.detail


def test_update_tag_bad_id(
    fake_tag: dict[str, Any],
    tag_command_usecase: TagCommandUseCaseImpl,
    tag_query_usecase: TagQueryUseCaseImpl,
) -> None:
    # Arrange

    tag_model = TagCreateModel.model_validate(fake_tag)
    tag = tag_command_usecase.create_tag(
        tag_model,
    )
    assert tag is not None
    updated_tag = TagUpdateModel.model_validate(tag.model_dump())

    try:
        tag_command_usecase.update_tag("bad_id", updated_tag)
        assert False
    except TagNotFoundError as e:
        assert e.status_code == TagNotFoundError.status_code
        assert e.detail == TagNotFoundError.detail

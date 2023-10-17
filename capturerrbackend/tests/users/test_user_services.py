from typing import Any

from sqlalchemy.orm import Session

from capturerrbackend.app.infrastructure.sqlite.user import UserQueryServiceImpl

# from ..app.infrastructure.dependencies import user_command_usecase, user_query_usecase
from capturerrbackend.app.usecase.user import (
    UserCommandUseCaseImpl,
    UserCreateModel,
    UserQueryService,
)


def test_user_query_service(
    db_fixture: Session,
    user_command_usecase: UserCommandUseCaseImpl,
    fake_user: dict[str, Any],
) -> None:
    user_query_service: UserQueryService = UserQueryServiceImpl(db_fixture)
    assert isinstance(user_query_service, UserQueryServiceImpl)

    # create 1st user
    user_model = UserCreateModel.model_validate(fake_user)
    user = user_command_usecase.create_user(
        user_model,
    )
    assert user is not None
    test_id = user.id
    test_user_name = user.user_name

    # create 2nd user
    fake_user["user_name"] = "linzc1st"
    user_model2 = UserCreateModel.model_validate(fake_user)
    user = user_command_usecase.create_user(
        user_model2,
    )
    assert user is not None
    new_user = user_query_service.find_by_id(test_id)
    assert new_user is not None
    assert new_user.id == test_id

    new_user = user_query_service.find_by_user_name(user_name=test_user_name)
    assert new_user is not None
    assert new_user.id == test_id

    users = user_query_service.find_all()
    assert len(users) == 2

    assert users[0].first_name == fake_user["first_name"]
    assert users[0].id == test_id

    assert users[1].user_name == fake_user["user_name"]

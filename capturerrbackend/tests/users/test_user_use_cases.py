from typing import Any

from capturerrbackend.app.domain.user.user_exception import (
    UserBadCredentialsError,
    UserNameAlreadyExistsError,
)
from capturerrbackend.app.usecase.user import (
    UserCommandUseCaseImpl,
    UserCreateModel,
    UserLoginModel,
    UserQueryUseCaseImpl,
)


def test_create_user(
    fake_user: dict[str, Any],
    user_command_usecase: UserCommandUseCaseImpl,
    user_query_usecase: UserQueryUseCaseImpl,
) -> None:
    # Arrange

    user_model = UserCreateModel.model_validate(fake_user)
    user = user_command_usecase.create_user(
        user_model,
    )
    assert user is not None

    all_users = user_query_usecase.fetch_users()
    assert len(all_users) > 0
    assert all_users[0].first_name == fake_user["first_name"]


def test_create_super_user(
    fake_super_user: dict[str, Any],
    user_command_usecase: UserCommandUseCaseImpl,
    user_query_usecase: UserQueryUseCaseImpl,
) -> None:
    # Arrange

    user_model = UserCreateModel.model_validate(fake_super_user)
    user = user_command_usecase.create_user(
        user_model,
    )
    assert user is not None

    all_users = user_query_usecase.fetch_users()
    assert len(all_users) > 0
    assert all_users[0].is_superuser is True


def test_create_user_duplicate_username(
    fake_user: dict[str, Any],
    user_command_usecase: UserCommandUseCaseImpl,
) -> None:
    # Arrange

    user_model = UserCreateModel.model_validate(fake_user)
    user = user_command_usecase.create_user(
        user_model,
    )
    assert user is not None
    try:
        # add the same user again
        user_command_usecase.create_user(
            user_model,
        )
        assert True is False
    except UserNameAlreadyExistsError as e:
        assert e.detail == UserNameAlreadyExistsError.detail
    except:
        assert True is False
        raise


def test_login_query_usecase(
    fake_user: dict[str, Any],
    user_command_usecase: UserCommandUseCaseImpl,
    user_query_usecase: UserQueryUseCaseImpl,
) -> None:
    # create user
    user_model = UserCreateModel.model_validate(fake_user)
    user_command_usecase.create_user(
        user_model,
    )

    # login
    data = {"user_name": "matt", "password": "matt"}
    u = UserLoginModel.model_validate(data)
    user = user_query_usecase.login_user(u)
    assert user is not None


def test_login_query_usecase_bad_password(
    fake_user: dict[str, Any],
    user_command_usecase: UserCommandUseCaseImpl,
    user_query_usecase: UserQueryUseCaseImpl,
) -> None:
    # create user
    user_model = UserCreateModel.model_validate(fake_user)
    user_command_usecase.create_user(
        user_model,
    )

    # login
    data = {"user_name": "matt", "password": "incorrect password"}
    u = UserLoginModel.model_validate(data)
    try:
        user_query_usecase.login_user(u)
    except UserBadCredentialsError:
        assert True
    except:
        assert True is False
        raise

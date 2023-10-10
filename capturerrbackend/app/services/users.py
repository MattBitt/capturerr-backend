"""
_summary_
"""
from typing import Annotated, Optional, Union

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from capturerrbackend.app.repos.users import UserRepo
from capturerrbackend.app.schemas.token import TokenRequest
from capturerrbackend.app.schemas.user import UserRequest, UserResponse
from capturerrbackend.app.settings import settings
from capturerrbackend.core.security import oauth2_scheme  # type: ignore
from capturerrbackend.core.security import verify_password


class UserService:
    """
    _summary_
    """

    def __init__(self, repo: UserRepo) -> None:
        """
        _summary_

        Args:
            repo (UserRepo): _description_
        """
        self.user_repo = repo

    def create(self, user_data: UserRequest) -> UserResponse:
        """
        _summary_

        Args:
            user_data (UserRequest): _description_

        Returns:
            UserResponse: _description_
        """
        user = self.user_repo.create_new_user(user_data)
        return user

    def get_user(self, username: str) -> Optional[UserResponse]:
        """
        _summary_

        Args:
            username (str): _description_

        Returns:
            Optional[UserResponse]: _description_
        """
        user = self.user_repo.get_by_username(username)
        return user

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> Union[UserResponse, bool]:
        """
        _summary_

        Args:
            username (str): _description_
            password (str): _description_

        Returns:
            Union[UserResponse, bool]: _description_
        """
        user = self.user_repo.get_by_username(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user


user_repo = UserRepo()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserResponse:
    """
    _summary_

    Args:
        token (Annotated[str, Depends): _description_

    Raises:
        credentials_exception: _description_
        credentials_exception: _description_
        credentials_exception: _description_

    Returns:
        UserResponse: _description_
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithim],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenRequest(username=username)
    except JWTError as exc:
        raise credentials_exception from exc
    user = user_repo.get_by_username(username=token_data.username)  # type: ignore
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserRequest, Depends(get_current_user)],
) -> UserResponse:
    """
    _summary_

    Args:
        current_user (Annotated[UserRequest, Depends): _description_

    Raises:
        HTTPException: _description_

    Returns:
        UserResponse: _description_
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return UserResponse.model_validate(current_user)

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from capturerrbackend.app.dao.users import UserRepo
from capturerrbackend.app.schemas.token import TokenResponse
from capturerrbackend.app.services.users import UserService
from capturerrbackend.app.settings import settings
from capturerrbackend.core.security import create_access_token

router = APIRouter()

user_repo = UserRepo()


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    token = UserService(user_repo=user_repo).authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires,
    )
    return TokenResponse.model_validate(
        {"access_token": access_token, "token_type": "bearer"},
    )

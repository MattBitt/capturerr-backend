from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from loguru import logger
from passlib.context import CryptContext
from pydantic import BaseModel

from capturerrbackend.config.configurator import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class DataToken(BaseModel):
    id: Optional[str] = None


class TokenData(BaseModel):
    user_name: str | None = None


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(non_hashed_pass: str, hashed_pass: str) -> bool:
    return pwd_context.verify(non_hashed_pass, hashed_pass)


def create_access_token(data: dict[str, str]) -> str:
    logger.debug(f"Creating access token from {data}")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.access_token_expire_minutes)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, config.secret_key, config.algorithm)

    return encoded_jwt

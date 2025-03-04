"""
User logic
"""

from typing import Annotated
from secrets import compare_digest

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from models.user import User
from database.db import get_session
from .crud import get_user

from crypto import hash_password


security = HTTPBasic()


def password_check(hashed_password: str, request_password: str) -> bool:
    """Compares hashed and request password strings"""
    return compare_digest(hashed_password, hash_password(request_password))


async def auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    session: AsyncSession = Depends(get_session),
) -> User:
    """Auth by username and password"""
    user = await get_user(session, credentials.username)
    if user and password_check(user.hashed_password, credentials.password):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password!",
        headers={"WWW-Authenticate": "basic"},
    )

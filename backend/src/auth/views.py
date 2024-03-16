"""
Auth views
"""
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from backend.src.database.db import get_session
from backend.src.models.user import User
from .security import get_user, password_check, verify_admin, create_user


router = APIRouter(tags=["User auth"])
security = HTTPBasic()


unauth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password!",
    headers={"WWW-Authenticate": "basic"}
)


@router.get("/login", status_code=status.HTTP_200_OK)
async def auth_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                           session: AsyncSession = Depends(get_session)):
    """Auth by username and password"""
    user = await get_user(session, credentials.username)
    if user and password_check(user.hashed_password, credentials.password):
        return status.HTTP_200_OK
    raise unauth_exception


@router.post("/register", response_model=User)
async def register_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                        user_to_register: HTTPBasicCredentials,
                        session: AsyncSession = Depends(get_session)) -> User:
    """Register user. Only admin can register new users"""
    if not verify_admin(credentials):
        raise unauth_exception

    created_user = await create_user(session, user_to_register)

    if not created_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this username already exists!")

    return created_user



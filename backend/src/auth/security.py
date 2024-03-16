"""
User auth logic
"""
from secrets import compare_digest

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import select

from fastapi.security import HTTPBasicCredentials

from .crypto import hash_password
from backend.src.models.user import User
from backend.src.constants import ADMIN_USERNAME, ADMIN_PASSWORD


def password_check(hashed_password: str, request_password: str) -> bool:
    """Compares hashed and request password strings"""
    return compare_digest(hashed_password, hash_password(request_password))


async def get_user(session: AsyncSession, username: str) -> User | None:
    """Returns user by username"""
    result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def create_user(session: AsyncSession, user: HTTPBasicCredentials) -> User | None:
    """Creates user"""
    existing_user = await session.execute(select(User).where(User.username == user.username))
    if existing_user.scalars().first():
        return
    new_user = User(username=user.username, hashed_password=hash_password(user.password))
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


def verify_admin(user: HTTPBasicCredentials) -> bool:
    """Compares user credentials to admin credentials"""
    hashed_admin_password = hash_password(ADMIN_PASSWORD)
    hashed_password = hash_password(user.password)
    if compare_digest(user.username, ADMIN_USERNAME) and compare_digest(hashed_password, hashed_admin_password):
        return True
    return False

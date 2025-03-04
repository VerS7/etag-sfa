"""
Create
Read
Update
Delete
"""

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import select

from fastapi.security import HTTPBasicCredentials

from crypto import hash_password
from models.user import User


async def get_users(session: AsyncSession) -> list[User]:
    """get all"""
    result = await session.execute(select(User).order_by(User.id))
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, username: str) -> User | None:
    """get one by username"""
    result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def add_user(session: AsyncSession, user: HTTPBasicCredentials) -> User:
    """add user by schema"""
    existing_user = await session.execute(
        select(User).where(User.username == user.username)
    )

    if existing_user.scalars().first():
        raise ValueError("User with this username already exists!")

    new_user = User(
        username=user.username, hashed_password=hash_password(user.password)
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def update_user(
    session: AsyncSession, user: User, user_update: HTTPBasicCredentials
) -> User:
    """update user"""
    pass


async def delete_user(session: AsyncSession, user: User) -> None:
    """delete user"""
    await session.delete(user)
    await session.commit()

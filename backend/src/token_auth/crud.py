"""
Create
Read
Update
Delete
"""

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import select

from models.token import AuthToken
from crypto import hash_func


async def create_token(session: AsyncSession, name: str) -> AuthToken:
    """Create auth token"""
    token = await session.execute(select(AuthToken).where(AuthToken.name == name))
    if token.scalars().first():
        raise ValueError("Token with this name already exists!")

    new_token = AuthToken(name=name, token=hash_func(name))
    session.add(new_token)
    await session.commit()

    return new_token


async def get_token(session: AsyncSession, name: str) -> AuthToken:
    """Get auth token"""
    token = await session.execute(select(AuthToken).where(AuthToken.name == name))
    return token.scalars().first()


async def verify_token(session: AsyncSession, token: str) -> AuthToken | None:
    """Verify token by token string"""
    verified_token = await session.execute(
        select(AuthToken).where(AuthToken.token == token)
    )
    return verified_token.scalar()


async def get_tokens(session: AsyncSession) -> list[AuthToken]:
    """Get auth tokens"""
    tokens = await session.execute(select(AuthToken))
    return list(tokens.scalars().all())


async def update_token(session: AsyncSession) -> AuthToken:
    """Update token"""
    pass


async def delete_token(session: AsyncSession, token: AuthToken) -> None:
    """Delete token"""
    await session.delete(token)

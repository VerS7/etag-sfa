"""
Admin logic
"""
from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import select

from backend.src.auth.crypto import hash_password
from backend.src.models.user import User
from constants import ADMIN_USERNAME, ADMIN_PASSWORD


async def init_admin(session: AsyncSession) -> None:
    """Initialize admin into DB"""
    result = await session.execute(select(User).where(User.id == 0))
    if not result.scalar():
        session.add(User(id=0, username=ADMIN_USERNAME, hashed_password=hash_password(ADMIN_PASSWORD), role="admin"))
        await session.commit()

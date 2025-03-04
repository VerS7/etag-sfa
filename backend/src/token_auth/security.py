"""
Token logic
"""

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status

from database.db import get_session
from models.token import AuthToken
from token_auth.crud import verify_token


async def token_auth(
    token: str, session: AsyncSession = Depends(get_session)
) -> AuthToken:
    """Auth by token"""
    verified_token = await verify_token(session, token)
    if verified_token:
        return verified_token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token!"
    )

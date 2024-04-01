"""
Token auth views
"""
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status

from backend.src.database.db import get_session
from backend.src.models.user import User
from backend.src.models.token import AuthToken
from backend.src.user_auth.security import auth_credentials

from . import crud

router = APIRouter(prefix="/token", tags=["Token Auth"], dependencies=[Depends(auth_credentials)])


@router.post("/", response_model=AuthToken)
async def create_token(token_name: str,
                       credentials: User = Depends(auth_credentials),
                       session: AsyncSession = Depends(get_session)) -> AuthToken:
    """Create token endpoint. Only admin can create new tokens"""
    if not credentials.role == "admin":
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="User without admin role can't create tokens!")

    try:
        created_token = await crud.create_token(session, token_name)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Token with this username already exists!")

    return created_token


@router.get("/", response_model=list[AuthToken])
async def get_tokens(session: AsyncSession = Depends(get_session)):
    """Get all tokens endpoint"""
    tokens = await crud.get_tokens(session)
    if len(tokens) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tokens not found!")
    return tokens


@router.get("/{name}", response_model=AuthToken)
async def get_token(name: str,
                    session: AsyncSession = Depends(get_session)):
    """Get token by name endpoint"""
    token = await crud.get_token(session, name)
    if token is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Token with this name not found!")
    return token

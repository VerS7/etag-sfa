"""
Auth views
"""
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials

from database.db import get_session
from models.user import User
from . import crud
from .security import auth_credentials


router = APIRouter(tags=["User Auth"])


@router.get("/login", response_model=User)
async def login(user: User = Depends(auth_credentials)):
    """Login user"""
    return user


@router.post("/register", response_model=User)
async def register_user(user_to_register: HTTPBasicCredentials,
                        credentials: User = Depends(auth_credentials),
                        session: AsyncSession = Depends(get_session)) -> User:
    """Register user. Only admin can register new users"""
    if not credentials.role == "admin":
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="User without admin role can't create other users!")

    try:
        created_user = await crud.add_user(session, user_to_register)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="User with this username already exists!")

    return created_user

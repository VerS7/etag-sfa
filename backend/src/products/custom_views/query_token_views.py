"""
Product custom_views
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.db import get_session

from backend.src.token_auth.security import token_auth

from .. import crud
from ..schemas import Product


router = APIRouter(dependencies=[Depends(token_auth)])


@router.get("/{token}", response_model=list[Product])
async def get_products(session: AsyncSession = Depends(get_session)):
    """get all products endpoint"""
    return await crud.get_products(session)


@router.get("/{token}/{product_id}/", response_model=Product)
async def get_product(product_id: int,
                      session: AsyncSession = Depends(get_session)):
    """get products by id endpoint"""
    product = await crud.get_product(session, product_id)
    if product is not None:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

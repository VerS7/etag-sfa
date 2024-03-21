"""
Product views
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.db import get_session

from backend.src.token_auth.security import token_auth
from backend.src.user_auth.security import auth_credentials

from backend.src.models.token import AuthToken
from backend.src.models.user import User

from . import crud
from .schemas import Product, ProductCreate, ProductUpdatePartial


router = APIRouter(prefix="/product", tags=["Products"])


@router.get("/", response_model=list[Product])
async def get_products(session: AsyncSession = Depends(get_session),
                       user_access: User = Depends(auth_credentials)):
    """get all products endpoint"""
    return await crud.get_products(session)


@router.get("/{product_id}/", response_model=Product)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session),
                      user_access: User = Depends(auth_credentials)):
    """get products by id endpoint"""
    product = await crud.get_product(session, product_id)
    if product is not None:
        return product
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/{token}", response_model=list[Product])
async def get_products(session: AsyncSession = Depends(get_session),
                       token_access: AuthToken = Depends(token_auth)):
    """get all products endpoint"""
    return await crud.get_products(session)


@router.get("/{token}/{product_id}/", response_model=Product)
async def get_product(product_id: int,
                      session: AsyncSession = Depends(get_session),
                      token_access: AuthToken = Depends(token_auth)):
    """get products by id endpoint"""
    product = await crud.get_product(session, product_id)
    if product is not None:
        return product
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_session),
                         user_access: User = Depends(auth_credentials)):
    """create product endpoint"""
    return await crud.add_product(session, product)


@router.put("/{product_id}/")
async def update_product_partial(product_id: int,
                                 product_update: ProductUpdatePartial,
                                 session: AsyncSession = Depends(get_session),
                                 user_access: User = Depends(auth_credentials)):
    """update product endpoint"""
    product = await crud.get_product(session, product_id)
    if product is not None:
        return await crud.update_product(
            session,
            product,
            product_update,
            partial=True
        )
    return HTTPException(status_code=404, detail="Item not found")


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int,
                         session: AsyncSession = Depends(get_session),
                         user_access: User = Depends(auth_credentials)):
    """delete product endpoint"""
    product = await crud.get_product(session, product_id)
    if product is not None:
        return await crud.delete_product(session, product)
    return HTTPException(status_code=404, detail="Item not found")

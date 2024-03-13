"""
Product views
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.db import get_session
from . import crud
from .schemas import Product, ProductCreate, ProductUpdatePartial


router = APIRouter(prefix="/product", tags=["Products"])


@router.get("/", response_model=list[Product])
async def get_products(session: AsyncSession = Depends(get_session)):
    """get all products endpoint"""
    return await crud.get_products(session)


@router.get("/{product_id}/", response_model=Product)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    """get products by id endpoint"""
    product = await crud.get_product(session, product_id)
    if product is not None:
        return product
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_session)):
    """create product endpoint"""
    return await crud.add_product(session, product)


@router.put("/{product_id}/")
async def update_product_partial(product_id: int,
                                 product_update: ProductUpdatePartial,
                                 session: AsyncSession = Depends(get_session)
                                 ):
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
                         session: AsyncSession = Depends(get_session)
                         ):
    """delete product endpoint"""
    product = await crud.get_product(session, product_id)
    if product is not None:
        return await crud.delete_product(session, product)
    return HTTPException(status_code=404, detail="Item not found")

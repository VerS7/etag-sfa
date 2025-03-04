"""
Product user access views
"""

from fastapi import APIRouter, HTTPException, status, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_pagination import Page, paginate

from database.db import get_session
from user_auth.security import auth_credentials
from image.generating import generate_image

from .. import crud
from ..schemas import Product, ProductCreate, ProductUpdatePartial


router = APIRouter(dependencies=[Depends(auth_credentials)], tags=["User Access"])


@router.get("/", response_model=Page[Product])
async def get_products(session: AsyncSession = Depends(get_session)):
    """get paginated products endpoint"""
    return paginate(await crud.get_products(session))


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, session: AsyncSession = Depends(get_session)
):
    """create product endpoint"""
    return await crud.add_product(session, product)


@router.put("/{product_id}/")
async def update_product_partial(
    product_id: int,
    product_update: ProductUpdatePartial,
    session: AsyncSession = Depends(get_session),
):
    """update product endpoint"""
    product = await crud.get_product(session, product_id)
    if product is not None:
        return await crud.update_product(session, product, product_update, partial=True)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    """delete product endpoint"""
    product = await crud.get_product(session, product_id)
    if product is not None:
        return await crud.delete_product(session, product)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.get("/image/{product_id}/", response_class=Response)
async def get_product_image(
    product_id: int,
    scale: float = None,
    size: str = None,
    session: AsyncSession = Depends(get_session),
):
    """Returns product image bytes by id"""
    product = await crud.get_product(session, product_id)

    if product is not None:
        return Response(
            content=await generate_image("default", product, scale=scale, size=size),
            media_type="image/png",
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!"
    )

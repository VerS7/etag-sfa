"""
Product query token access views
"""
from fastapi import APIRouter, HTTPException, status, Depends, Response

from fastapi_pagination import Page, paginate

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.db import get_session
from backend.src.token_auth.security import token_auth
from backend.src.image.generating import generate_image

from .. import crud
from ..schemas import Product, ProductCreate


router = APIRouter(dependencies=[Depends(token_auth)])


@router.get("/{token}", response_model=Page[Product])
async def get_products(session: AsyncSession = Depends(get_session)):
    """get paginated products endpoint"""
    return paginate(await crud.get_products(session))


@router.get("/{token}/{product_id}/", response_model=Product)
async def get_product(product_id: int,
                      session: AsyncSession = Depends(get_session)):
    """get products by id endpoint"""
    product = await crud.get_product(session, product_id)
    if product is not None:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.post("/{token}", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_session)):
    """create product endpoint"""
    return await crud.add_product(session, product)


@router.get("/image/{token}/{product_id}/", response_class=Response)
async def get_product_image(product_id: int, session: AsyncSession = Depends(get_session)):
    """Returns product image bytes by id"""
    product = await crud.get_product(session, product_id)

    if product is not None:
        return Response(content=await generate_image("default", product), media_type="image/png")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Product not found!")
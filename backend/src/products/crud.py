"""
Create
Read
Update
Delete
"""
from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import select

from backend.src.models.product import Product
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial


async def get_products(session: AsyncSession) -> list[Product]:
    """get all"""
    result = await session.execute(select(Product).order_by(Product.id))
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    """get one by id"""
    return await session.get(Product, product_id)


async def add_product(session: AsyncSession, product: ProductCreate) -> Product:
    """add product by schema"""
    product = Product(**product.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def update_product(session: AsyncSession,
                         product: Product,
                         product_update: ProductUpdate | ProductUpdatePartial,
                         partial: bool = False
                         ) -> Product:
    """update product"""
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: Product) -> None:
    """delete product"""
    await session.delete(product)
    await session.commit()

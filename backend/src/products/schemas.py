"""
Product schemas
"""
from decimal import Decimal

from pydantic import BaseModel


class ProductBase(BaseModel):
    """Base product schema"""
    name: str
    price: Decimal
    sale_price: Decimal | None
    category: str | None
    subcategory: str | None
    brand: str | None
    unit: str | None
    producer: str | None
    producer_country: str | None


class ProductCreate(ProductBase):
    """Create product schema"""
    pass


class ProductUpdate(ProductCreate):
    """Update product schema"""
    pass


class ProductUpdatePartial(ProductBase):
    """Partial update product schema"""
    name: str | None
    price: str | None


class Product(ProductBase):
    """Product schema"""
    id: int

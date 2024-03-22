"""
Product models
"""
from decimal import Decimal

from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    """Product model"""
    __tablename__ = "products"
    id: int = Field(primary_key=True, index=True)
    name: str = Field()
    price: Decimal = Field()
    sale_price: Decimal | None = Field(default=None)
    category: str | None = Field(nullable=True)
    subcategory: str | None = Field(nullable=True)
    brand: str | None = Field(nullable=True)
    unit: str | None = Field(default="шт", nullable=True)
    producer: str | None = Field(nullable=True)
    producer_country: str | None = Field(nullable=True)

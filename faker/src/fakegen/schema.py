"""
Products
"""
from decimal import Decimal

from pydantic import BaseModel, Field


class Product(BaseModel):
    """Raw product"""
    name: str
    info: str
    brand: str
    producer: str 
    subcategory: str | None


class CompletedProduct(BaseModel):
    """Completed product for uploading"""
    barcode: str
    price: Decimal 
    sale_price: Decimal | None 
    category: str | None 
    subcategory: str | None
    brand: str | None
    unit: str | None = Field(default="шт")
    producer: str | None
    producer_country: str | None

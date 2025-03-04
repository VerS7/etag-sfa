"""
Products
"""

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

    name: str
    barcode: str
    price: str
    sale_price: str | None
    category: str | None
    subcategory: str | None
    brand: str | None
    unit: str | None = Field(default="шт")
    producer: str | None
    producer_country: str | None

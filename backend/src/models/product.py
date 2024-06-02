"""
Product models
"""
from datetime import datetime

from sqlmodel import SQLModel, Field, Column

from sqlalchemy import DateTime


class Product(SQLModel, table=True):
    """Product model"""
    __tablename__ = "products"
    id: int = Field(primary_key=True, index=True)
    name: str = Field()
    price: str = Field()
    barcode: str = Field()
    sale_price: str | None = Field(default=None)
    category: str | None = Field(nullable=True)
    subcategory: str | None = Field(nullable=True)
    brand: str | None = Field(nullable=True)
    unit: str | None = Field(default="шт", nullable=True)
    producer: str | None = Field(nullable=True)
    producer_country: str | None = Field(nullable=True)
    created_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True), default=datetime.utcnow()))
    updated_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True), onupdate=datetime.utcnow()))

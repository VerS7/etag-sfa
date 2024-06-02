"""
Product data generating
"""
from typing import Callable, Iterator
from decimal import Decimal
from random import random

from .schema import Product, CompletedProduct


class ProductBuilder:
    """Product data builder"""
    def __init__(self,
                 data: list[dict],
                 barcode_generator: Callable[[], str],
                 price_multiplier: float,
                 sale_chance: float,
                 sale_multiplier: float):
        self._brg = barcode_generator
        self._pm = price_multiplier
        self._sc = sale_chance
        self._sm = sale_multiplier

        self._data = data
        self._items = iter(self._generate_items())

    def _generate_items(self) -> list[dict]:
        named_items = []
        for block in self._data:
            for category, items in block.items():
                for item in items:
                    named_items.append({category: item})
        return named_items

    def _generate_price(self, min_price: Decimal) -> str:
        if self._pm < 1:
            raise ValueError(f"{self._pm=} is lower than 1.")

        return str((min_price * Decimal(self._pm)).quantize(Decimal("1.00")))

    def _generate_sale_price(self, min_price: Decimal) -> str | None:
        if self._sm > 0.99 or self._sm <= 0:
            raise ValueError(f"{self._sm} is incorrect.")

        if self._sc < 0 or self._sc > 1:
            raise ValueError(f"{self._sm} is incorrect.")

        if random() < self._sc:
            return str((min_price - (min_price * Decimal(self._sm))).quantize(Decimal("1.00")))
        return None

    def _generate(self, schema):
        for category, item in next(self._items).items():
            if schema is Product:
                return schema(
                    name=item["наименование"],
                    info=item["дополнительная информация"],
                    brand=item["бренд"],
                    producer=item["изготовитель"] if "изготовитель" in item.keys() else "Россия",
                    subcategory=item["подкатегория"] if "подкатегория" in item.keys() else None
                )
            if schema is CompletedProduct:
                return schema(
                    category=category,
                    barcode=self._brg(),
                    price=self._generate_price(item["минимальная цена"]),
                    sale_price=self._generate_sale_price(item["минимальная цена"]),
                    name=item["наименование"],
                    info=item["дополнительная информация"],
                    brand=item["бренд"],
                    producer_country=item["страна"] if "страна" in item.keys() else "Россия",
                    unit=item["единицы измерения"] if "единицы измерения" in item.keys() else "шт",
                    producer=item["изготовитель"] if "изготовитель" in item.keys() else None,
                    subcategory=item["подкатегория"] if "подкатегория" in item.keys() else None
                )

    def generate_completed_product(self) -> Iterator[CompletedProduct]:
        """Completed product iterator"""
        yield self._generate(CompletedProduct)

    def generate_product(self) -> Iterator[Product]:
        """Product iterator"""
        yield self._generate(Product)

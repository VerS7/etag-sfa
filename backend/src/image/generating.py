"""
Product image generating
"""

from models.product import Product

from .templates import DefaultImage


TEMPLATES = {"default": DefaultImage()}


async def generate_image(template: str, data: Product, **kwargs) -> bytes:
    """Generate .png image of product by template"""
    template_ = TEMPLATES.get(template, None)
    if template_ is None:
        raise ValueError(f"{template} is not implemented!")

    size = kwargs.get("size", None)
    scale = kwargs.get("scale", None)

    return await template_.generate_image(data=data, size=size, scale=scale)

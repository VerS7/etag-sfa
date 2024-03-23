"""
Image generating template
"""
from abc import ABCMeta, abstractmethod, ABC
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw

from backend.src.models.product import Product


class BaseImageTemplate(ABC, metaclass=ABCMeta):
    """Base image generating template"""
    def __init__(self, data):
        self.data = data

    @abstractmethod
    async def generate_image(self, *args, **kwargs):
        """Generate image"""
        pass


class DefaultImage(BaseImageTemplate):
    def __init__(self, data: Product):
        super().__init__(data)
        self.product_name_font = ImageFont.truetype("calibri", 20)
        self.company_name_font = ImageFont.truetype("calibri", 12)
        self.price_font = ImageFont.truetype("calibri", 50)
        self.info_font = ImageFont.truetype("calibri", 10)

    async def generate_image(self, size: tuple[int, int] | None = None, scale: float | None = None) -> bytes:
        if size is not None and size[0] <= 0 and size[1] <= 0:
            raise ValueError("Incorrect size.")

        color = (0, 0, 0)
        img = Image.open("image/assets/default.png")
        draw = ImageDraw.Draw(img)

        draw.text(text=self.data.name, font=self.product_name_font, xy=(10, 40), fill=color)
        draw.text(text=str(self.data.price), font=self.price_font, xy=(75, 80), fill=color)

        if size is not None:
            img.resize(size)

        img_bytes = BytesIO()
        img.save(img_bytes, format=img.format)

        return img_bytes.getvalue()

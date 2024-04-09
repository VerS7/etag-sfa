"""
Image generating template
"""
import os

from abc import ABCMeta, abstractmethod, ABC
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw

from backend.src.models.product import Product

from .utils import validate_img_size, validate_img_scale, draw_justified_text


class BaseImageTemplate(ABC, metaclass=ABCMeta):
    """Base image generating template"""
    @abstractmethod
    async def generate_image(self, *args, **kwargs) -> bytes:
        """Generate image"""
        pass


class DefaultImage(BaseImageTemplate):
    def __init__(self):
        print()
        self.bg_image = os.path.join(os.path.dirname(__file__), "assets/default/default.png")
        self.font = os.path.join(os.path.dirname(__file__), "assets/default/tahoma.ttf")
        self.bold_font = os.path.join(os.path.dirname(__file__), "assets/default/tahoma_bold.ttf")

        self.text_color = (0, 0, 0)

        self.product_name_font = ImageFont.truetype(self.bold_font, 45)
        self.price_font = ImageFont.truetype(self.bold_font, 120)
        self.info_font = ImageFont.truetype(self.bold_font, 40)
        self.sub_info_font = ImageFont.truetype(self.bold_font, 20)

    async def generate_image(self, data: Product, size: str | None = None, scale: float | None = None) -> bytes:
        """Generate image bytes from data with optional size and scale"""
        if size is not None and not validate_img_size(size):
            raise ValueError("Incorrect size.")

        if scale is not None and not validate_img_scale(scale):
            raise ValueError("Incorrect scale.")

        bg_image = Image.open(self.bg_image)
        draw = ImageDraw.Draw(bg_image)
        # Единица измерения
        draw.text(text=f"{data.price:.2f}",
                  font=self.price_font,
                  xy=(bg_image.size[0] / 2, 450),
                  fill=self.text_color,
                  anchor="mm")
        # Цена продукта
        draw.text(text=f"{data.unit if '.' in data.unit else f'{data.unit}.'}",
                  font=self.info_font,
                  xy=(90, 335),
                  fill=self.text_color,
                  anchor="mm")
        # Страна
        draw.text(text=data.producer_country,
                  font=self.info_font,
                  xy=(535, 560),
                  fill=self.text_color,
                  anchor="rm")
        # Наименование продукта
        draw_justified_text(draw,
                            text=data.name,
                            font=self.product_name_font,
                            xy=(int(bg_image.size[0] / 2), 150),
                            fill=self.text_color,
                            anchor="mm",
                            line_width=17)
        # Производитель
        draw_justified_text(draw,
                            text=data.producer,
                            font=self.sub_info_font,
                            xy=(15, 565),
                            fill=self.text_color,
                            anchor="lm",
                            line_width=25,
                            margin=5,
                            reverse=True)

        if size is not None:
            bg_image = bg_image.resize((int(size.split("x")[0]), int(size.split("x")[1])))

        if scale is not None:
            bg_image = bg_image.resize((int(bg_image.size[0] * scale), int(bg_image.size[1] * scale)))

        img_bytes = BytesIO()
        bg_image.save(img_bytes, format="png")

        return img_bytes.getvalue()

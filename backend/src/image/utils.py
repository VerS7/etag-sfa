"""
Image generating utility functions
"""

import re
import textwrap

from PIL import ImageDraw, ImageFont


def validate_img_size(size: str) -> bool:
    """Validate image size. Example: '150x150' -> True; '-1x1' - False; '2313131' - False"""
    pattern = r"^\d+x\d+$"
    match = re.match(pattern, size)
    if match:
        width, height = size.split("x")
        return int(width) > 0 and int(height) > 0
    else:
        return False


def validate_img_scale(scale: float) -> bool:
    """Validate image scale"""
    return scale >= 0


def draw_justified_text(
    draw: ImageDraw,
    text: str,
    font: ImageFont,
    xy: tuple[int, int],
    fill: tuple[int, int, int],
    anchor: str,
    line_width: int,
    margin: int = 10,
    reverse: bool = False,
) -> None:
    """Draw justified text by line width in chars and margin"""
    x, y, x1, y1 = draw.textbbox(text=text, font=font, xy=xy)
    text_height = abs(y - y1)

    lines = textwrap.wrap(text, width=line_width)

    if reverse:
        for i, line in enumerate(lines[::-1]):
            draw.text(
                (xy[0], xy[1] - (i * (text_height + margin))),
                line,
                font=font,
                fill=fill,
                anchor=anchor,
            )
    else:
        for i, line in enumerate(lines):
            draw.text(
                (xy[0], xy[1] + (i * (text_height + margin))),
                line,
                font=font,
                fill=fill,
                anchor=anchor,
            )

import numpy as np
from PIL import Image


def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    width = image_size[0] / tile_size[0]
    height = image_size[1] / tile_size[1]
    tiles = width * height
    ordering_set = set(ordering)
    ordering_range = {*range(len(ordering))}

    if width.is_integer() and height.is_integer() and ordering_set == ordering_range:
        return len(ordering) == tiles
    return False


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    image = Image.open(image_path)
    width, height = image.size
    if not valid_input((width, height), tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")

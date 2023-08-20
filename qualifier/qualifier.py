import math

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
    im = Image.open(image_path)
    width, height = im.size
    if not valid_input((width, height), tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")

    tile_width, tile_height = tile_size
    number_of_columns = width // tile_width
    # number_of_rows = height // tile_height

    result = Image.new(im.mode, (width, height))
    for i in ordering:
        n = ordering.index(i)

        new_column, new_row = get_position(n, number_of_columns)
        source_column, source_row = get_position(i, number_of_columns)

        new_locations = get_coordinates(new_row, new_column, tile_height, tile_width)
        source_locations = get_coordinates(source_row, source_column, tile_height, tile_width)

        tile = im.crop(source_locations)
        result.paste(tile, new_locations)

    result.show()
    result.save(out_path, 'PNG')


def get_coordinates(row, column, tile_height, tile_width) -> tuple[int, int, int, int]:
    """
    returns the coordinates (left, upper, right, lower) of a tile, given its position and a tiles size
    """
    left = column * tile_width
    right = left + tile_width
    upper = row * tile_height
    lower = upper + tile_height
    return left, upper, right, lower


def get_position(i, number_of_columns) -> tuple[int, int]:
    """
    returns the row/column numbers (0-indexed), given a tiles index
    and the number of columns
    """
    rows = math.floor(i / number_of_columns)
    cols = i - rows * number_of_columns
    return cols, rows

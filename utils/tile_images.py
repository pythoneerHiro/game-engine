from math import ceil
from typing import List, Tuple

import numpy as np
from icecream import ic
from PIL import Image


def genTilesFromImage(img: Image.Image, grid: Tuple[int, int] = (3, 3)) -> List[np.ndarray]:
    im = np.array(img)
    M = ceil(im.shape[0] / grid[0])
    N = ceil(im.shape[1] / grid[1])
    ic(im.shape, M, N, grid)
    tiles = [im[x:x + M, y:y + N] for x in range(0, im.shape[0], M) for y in range(0, im.shape[1], N)]
    ic(len(tiles))
    return tiles


def tilesToImages(tiles: List[np.ndarray]) -> List[Image.Image]:
    images = [Image.fromarray(tile) for tile in tiles]
    return images


def sliceImage1(img: Image.Image, grid: Tuple[int, int]) -> List[Image.Image]:
    tiles = genTilesFromImage(img, grid)
    tile_images = tilesToImages(tiles)
    return tile_images

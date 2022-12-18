import os
import random
import string
from typing import List, Tuple

from icecream import ic
from image_slicer import slice
from PIL import Image


def retrieveImage(url: str) -> Image.Image:
    import requests
    from io import BytesIO
    
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    ic(img.size, img.mode, img.format)
    return img


def sliceImage(img: Image.Image, grid: Tuple[int, int]) -> List[Image.Image]:
    folder = ''.join(random.choices(string.ascii_letters, k=6))
    out = f"../static/temp/{folder}"
    
    try:
        os.makedirs(out)
    except FileExistsError:
        return sliceImage(img)
    except Exception as e:
        ic(e)
        raise Exception("unable to create the folder due to Error", e)
    
    ic(out)
    
    src_image = f"{out}/orig.img"
    
    img.save(src_image)
    
    imgs = slice(src_image, grid[0] * grid[1])
    
    ic(len(imgs))
    
    return imgs

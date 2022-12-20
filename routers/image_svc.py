import os
from datetime import datetime
from typing import NamedTuple, Tuple

from dask import compute
from fastapi import APIRouter
from pydantic import BaseModel

from utils.image import retrieveImage, sliceImage
from utils.random import randomStringGen
from utils.upload_azure import uploadAzureBlobStorage

router = APIRouter(tags=["image  processing"])


class Grid(NamedTuple):
    row: int
    column: int


class Product(BaseModel):
    url: str
    grid: Tuple[int, int]  # FIXME pass Grid


@router.get("/")
async def home():
    return {"message": "image_svc up & running"}


@router.post("/tile")
async def create(product: Product):
    product_url = product.url
    
    product_img = retrieveImage(product_url)
    
    _images = sliceImage(product_img, product.grid)
    
    today = datetime.now().strftime("%d.%m.%Y.%H.%M.%S")
    
    today_seed = f"{today}-{randomStringGen(3)}"
    
    delayed_obj = []
    
    for i in _images:
        img = i.filename
        img_name = os.path.basename(img)
        img_format = img_name.split('.')[-1]
        custom_filename = f"{today_seed}-{img_name}"
        
        img_url = uploadAzureBlobStorage(img, custom_filename, f"image/{img_format}")
        delayed_obj.append(img_url)
    
    imgs = list(compute(delayed_obj))
    
    res = {
        "images": imgs
    }
    return res

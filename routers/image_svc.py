import os
from typing import NamedTuple, Tuple

from fastapi import APIRouter
from pydantic import BaseModel

from utils.image import retrieveImage, sliceImage
from utils.upload_azure import uploadAzureBlobStorage

router = APIRouter(tags=["image  processing"])

from datetime import datetime


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
    imgs = []
    
    res = {
        "images": imgs
    }
    
    product_url = product.url
    
    product_img = retrieveImage(product_url)
    
    _images = sliceImage(product_img, product.grid)
    
    today = datetime.now()
    
    today_formated = today.strftime("%d.%m.%Y %H:%M:%S")
    
    for i in _images:
        img = i.filename
        custom_filename = f"{today_formated}-{os.path.basename(img)}"
        
        img_url = uploadAzureBlobStorage(img, custom_filename)
        imgs.append(img_url)
    
    return res

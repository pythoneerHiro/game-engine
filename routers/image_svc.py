import os
from datetime import datetime
from io import BytesIO
from typing import List, NamedTuple, Tuple

from dask import compute
from fastapi import APIRouter
from pydantic import BaseModel

from utils.image import retrieveImage, sliceImage
from utils.random import randomStringGen
from utils.tile_images import sliceImage1
from utils.upload_azure import uploadAzureBlobStorage, uploadBlobDirectly

router = APIRouter(tags=["image  processing"])
router1 = APIRouter(tags=["image processing v1"])


class Grid(NamedTuple):
    row: int
    column: int


class Product(BaseModel):
    url: str
    grid: Tuple[int, int]  # FIXME pass Grid


class Images(BaseModel):
    images: List[str]
    grid: Tuple[int, int]


@router.get("/")
async def home():
    return {"message": "image_svc up & running"}


@router.post("/tile")
async def split(product: Product):
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
    
    imgs = compute(*delayed_obj)
    
    res = {
        "images": imgs
    }
    return res


@router.post("/join")
async def join(images: Images):
    from image_slicer import join
    
    from fastapi.responses import Response
    
    images = [retrieveImage(img) for img in images.images]
    
    combined_image = join(images)
    
    with BytesIO() as image_data:
        combined_image.save(image_data, format("jpeg"))
    
    return Response(content=image_data, media_type="image/jpeg")


@router1.post("/tile")
async def split(product: Product):
    product_url = product.url
    
    product_img = retrieveImage(product_url)
    
    _images = sliceImage1(product_img, product.grid)
    
    today = datetime.now().strftime("%d.%m.%Y.%H.%M.%S")
    today_seed = f"{today}-{randomStringGen(3)}"
    
    delayed_obj = []
    
    img_format = product_img.format
    
    for i in range(len(_images)):
        image = _images[i]
        img_name = f"{i}.{img_format}"
        custom_filename = f"{today_seed}-{img_name}"
        
        # with BytesIO() as image_data:
        #     image.save(image_data, format=img_format)
        #     data = output.getvalue()
        image_data = BytesIO()
        image.save(image_data, format=img_format)
        
        img_url = uploadBlobDirectly(image_data.getvalue(), custom_filename, f"image/{img_format}")
        delayed_obj.append(img_url)
    
    images = compute(*delayed_obj)
    
    res = {
        "images": images
    }
    return res

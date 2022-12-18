from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/imago', tags=['image  processing'])


class Product(BaseModel):
    url: str


@router.post("/")
async def create(product: Product):
    pass

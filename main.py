from os import environ

from fastapi import FastAPI
from fastapi.logger import logger
from icecream import ic
from requests import Request

from routers import image_svc

debug = environ.get("debug", False)

app = FastAPI(debug=debug)

app.include_router(image_svc.router, prefix="/image")
app.include_router(image_svc.router1, prefix="/image/v1")


@app.middleware("http")
async def log_stuff(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    req = await request.body()
    ic("Request", req)
    response = await call_next(request)
    logger.info(response.status_code)
    return response


@app.get("/")
async def root():
    return {"message": "game engine up and running"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app)

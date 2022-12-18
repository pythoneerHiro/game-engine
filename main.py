from fastapi import FastAPI

from routers import image_svc

app = FastAPI()
app.include_router(image_svc.router, prefix="/image")


@app.get("/")
async def root():
    return {"message": "game engine up and running"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app)

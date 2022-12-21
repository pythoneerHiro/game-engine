from dask import compute, delayed
from icecream import ic

from . import client


def test_home():
    response = client.get("/image")
    assert response.status_code == 200
    assert response.json() == {"message": "image_svc up & running"}


def test_create(grid=(2, 2)):
    import validators
    
    @delayed
    def _test_image_url(url: str):
        response = client.post(url, json={
            "url":  "https://static.wikia.nocookie.net/big-hero-6-fanon/images/0/0f/Hiro.jpg/revision/latest?cb=20180511180437",
            "grid": grid
        })
        
        assert response.status_code == 200
        
        res = response.json()
        
        images = res["images"]
        
        assert isinstance(images, list)
        
        assert len(images) == grid[0] * grid[1]
        
        for img_url in images:
            assert validators.url(img_url)
    
    urls = ["/image/tile", "/image/v1/tile"]
    
    delayed_obj = []
    
    for url in urls:
        d = _test_image_url(url)
        delayed_obj.append(d)
    compute(*delayed_obj)


def test_table_create():
    grids = [(2, 2), (3, 3), (4, 4)]
    
    delayed_obj = []
    
    for grid in grids:
        ic(grid)
        delayed_obj.append(test_create(grid))
    
    compute(*delayed_obj)

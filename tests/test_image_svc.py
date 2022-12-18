from icecream import ic

from . import client


def test_home():
    response = client.get("/image")
    assert response.status_code == 200
    assert response.json() == {"message": "image_svc up & running"}


def test_create(grid=(2, 2)):
    response = client.post("/image", json={
        "url":  "https://static.wikia.nocookie.net/big-hero-6-fanon/images/0/0f/Hiro.jpg/revision/latest?cb=20180511180437",
        "grid": grid
    })
    assert response.status_code == 200
    
    res = response.json()
    
    assert type(res["images"]) == 'list'
    
    assert len(res["images"]) == grid[0] * grid[1]


def test_table_create():
    grids = [(2, 2), (3, 3), (4, 4)]
    
    for grid in grids:
        ic(grid)
        test_create(grid)
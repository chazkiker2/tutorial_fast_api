from fastapi import FastAPI

from typing import Optional
from pydantic import BaseModel
from enum import Enum

#  tutorial part 1
app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {
        "item_name": item.name,
        "item_price": item.price,
        "item_id": item_id,
    }


@app.get("/users/me")
def read_user_me():
    return {"user_id": "current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# tutorial part 2

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {
            "model_name": model_name,
            "message": "Deep Learning FTW!",
        }
    if model_name.value == "lenet":
        return {
            "model_name": model_name,
            "message": "LeCNN all the images"
        }
    return {
        "model_name": model_name,
        "message": "Have some residuals"
    }


@app.get("/files/{file_path:path}")
async def read_line(file_path: str):
    return {
        "file_path": file_path,
    }


# tutorial part 3

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/fake_items/")
async def read_item(skip: int = 0, limit: int = 10):
    # when you declare other function parameters that aren't in path params,
    # they are automatically interpreted as "query" parameters
    return fake_items_db[skip: skip + limit]


# DEFAULT https://127.0.0.1:8000/items/?skip=0&limit=10
# as part of the URL, they are naturally strings. But when declared with Python types,
# they are converted to that type and validated against it

@app.get("/fake_items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {
        "item_id": item_id,
    }
    if q:
        item.update({
            "q": q,
        })
    if not short:
        item.update({
            "description": "This is an amazing item that has a long description"
        })

    return item

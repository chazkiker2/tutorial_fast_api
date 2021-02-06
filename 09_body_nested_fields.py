from typing import Optional, Set, List

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item1(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    # tags: list = []  # you can define an attribute to be a subtype. For example a Python `list`
    # tags: List[str] = []  # or a List with a type parameter
    tags: Set[str] = set()  # or a list of unique items, i.e., a Python set
    image: Optional[Image] = None  # Pydantic types can be other Pydantic Models


"""
WITH THE ABOVE ITEM MODEL, FastAPI would expect a body such as:

    {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2,
        "tags": ["rock", "metal", "bar"],
        "image": {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        }
    }
"""


@app.put("items_01/{item_id}")
async def update_item_01(item_id: int, item: Item1):
    results = {
        "item_id": item_id,
        "item": item,
    }

    return results


"""
# ATTRIBUTES WITH LISTS OF SUBMODELS

You can also use Pydantic models as sybtypes of list, set, etc.
"""


class Item2(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    images: Optional[List[Image]] = None


"""
The above model Item2 would requrie a body like so:

    {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2,
        "tags": [
            "rock",
            "metal",
            "bar"
        ],
        "images": [
            {
                "url": "http://example.com/baz.jpg",
                "name": "The Foo live"
            },
            {
                "url": "http://example.com/dave.jpg",
                "name": "The Baz"
            }
        ]
    }
"""


@app.put("items_02/{item_id}")
async def update_item_02(item_id: int, item: Item2):
    results = {
        "item_id": item_id,
        "item": item,
    }

    return results


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item2]  # you can even have arbitrarily deeply nested models


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

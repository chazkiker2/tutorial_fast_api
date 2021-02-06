from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

"""
SCHEMA EXTRA — EXAMPLE

You can define extra information to go in JSON Schema. 
A common use case is to add an example that will be shown in the docs.

There are several ways that you can declare extra JSON Schema information



1. Pydantic schema_extra
    You can declare an example for a Pydantic model using Config and schema_extra, as described in Pydantic's docs


"""


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2
            }
        }


app.put("/items/{item_id}")


async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

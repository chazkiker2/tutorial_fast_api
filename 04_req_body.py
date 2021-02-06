from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Declare data model as a class that inherits from BaseModel.
    We can use standard Python types for all attributes.

    When a model attribute has a default value, it is not required.
    Otherwise, it is required. Use None to make it just optional.
    """

    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# you can also declare body, path, and query params... all at the same time.
# FastAPI will recognize each of them and take the data from the correct place
#
# The function parameters will be recognized as follows:
#   - if the param is also declared in the path, it will be used as a path parameter
#   - if the param is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query param
#   - if the param is declared to be one of the type of a pydantic Model, it will be interpreted as a req body
@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})

    if item.tax:
        price_with_tax = item.price + item.tax
        result.update({"price_with_tax": price_with_tax})

    return result

from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

"""
##############################################################################################################
EXAMPLE 01 — Body - Fields
##############################################################################################################

The same way you can declare additional validation and metadata in path operation function parameters with 
`Query`, `Path`, `Body`, you can declare validation and metadata inside of Pydantic models using Pydantic's `Field`.

First, you have to `from pydantic import BaseModel, Field`. 

Then, you can use Field with model attributes. Field works the same way as Query, Path, and Body. 
It has all the same parameters, etc.
"""


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


@app.put("/items_01/{item_id}")
async def update_item_01(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

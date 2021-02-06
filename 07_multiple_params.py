from typing import Optional

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


"""
##############################################################################################################
# EXAMPLE 01 — MIX Path, Query, and Body PARAMETERS
##############################################################################################################
First, of course, you can mix Path, Query, and req body parameter declarations freely and FastAPI will know what to do
And you can also declare body params as option by setting the default to None:
"""


@app.put("/items_01/{item_id}")
async def update_item_01(
        *,
        item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
        q: Optional[str] = None,
        item: Optional[Item] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


"""
In this example, the path operations would expect a JSON body with the attributes of an `Item1`, like:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
"""

"""
##############################################################################################################
EXAMPLE 02 — Multiple Body Parameters
##############################################################################################################

You can also declare multiple body parameters, e.g., `item` and `user`.

In this case, FastAPI will notice that there are more than one body params in the function 
(two parameters that are Pydantic models). 
So, it will then use the parameter names as keys (field names) in the body, and expect a body like:

{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}

It will perform the validation of the compound data, and will document it like that for 
the OpenAPI schema and automatic docs.

"""


@app.put("/items_02/{item_id}")
async def update_item_02(
        item_id: int,
        item: Item,
        user: User,
):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


"""
##############################################################################################################
EXAMPLE 03 — Singular Values in Body
##############################################################################################################

The same way there is a `Query` and `Path` to define extra data for query and path parameters, 
FastAPI provides an equivalent `Body`.

For example, extending the previous model, you could decide that you want to have anther key `importance` 
in the same body, besides the `item` and `user`.

If you declare it as is, because it is a singular value, FastAPI will assume that it is a query parameter. 
But you can instruct FastAPI to treat is as another body key using `Body`:

In this case, FastAPI will expect a body like this:
------------------------------------------------
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
"""


@app.put("/items_03/{item_id}")
async def update_item_03(
        item_id: int,
        item: Item,
        user: User,
        importance: int = Body(...),
):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance,
    }

    return results

"""
##############################################################################################################
EXAMPLE 04 — Multiple body params and query
##############################################################################################################

Of course, you can also declare additional query parameters whenver you need to, additional to any body params.

As, by default, singular values are interpreted as query parameters, you don't
have to explicitly add a `Query`, you can just do:
    `q: Optional[str] = None`

"""

"""
##############################################################################################################
EXAMPLE 05 — Embed a single body parameter
##############################################################################################################

Let's say you only have a single `item` body parameter from a Pydantic model `Item1`. 

By default, FastAPI will then expect its body directly. 

But, if you want to expect a JSON with a key `item` and inside of it the model contents, as it does when you 
declare extra body parameters, you can use the special `Body` parameter `embed`.
    
    item: Item1 = Body(..., embed=True)


In that case, FastAPI will expect a body like: 

    {
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        }
    }


instead of 

    {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
"""
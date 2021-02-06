from typing import Optional, List
from fastapi import FastAPI, Query

app = FastAPI()


# ORIGINAL
# @app.get("/items/")
# async def read_items(q: Optional[str] = None):
#     results = {
#         "items": [
#             {"item_id": "Foo",},
#             {"item_id": "Bar",},
#         ]
#     }
#     if q:
#         results.update({"q": q})
#
#     return results


# ADDITIONAL VALIDATION
@app.get("/items/")
async def read_items(
        q: Optional[str] = Query(
            None,
            min_length=3,
            max_length=50,
            regex="^fixedquery$"
        ),
        required_q: str = Query(..., min_length=3)
):
    results = {
        "items": [
            {"item_id": "Foo", },
            {"item_id": "Bar", },
        ]
    }
    if q:
        results.update({
            "q": q,
            "req_q": required_q
        })

    return results


@app.get("/items_2")
async def read_items(
        q: Optional[List[str]] = Query(
            None,
            deprecated=True,
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        )
):
    query_items = {"q": q}
    return query_items

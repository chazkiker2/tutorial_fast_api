from typing import Optional
from fastapi import FastAPI, Cookie

app = FastAPI()

"""
You can define Cookie params the same way that you would define Query and Path parameters. 
Import cookie, declare Cookie parameters. 

Cookie is a "sister" class of Path and Query. It also inherits from the same common Param class. 

But remember when you import Query, Path, Cookie, and others from FastAPI, those are 
actually functions that return special classes.
"""


@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}

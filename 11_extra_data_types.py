from typing import Optional
from datetime import datetime, time, timedelta
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
        item_id: UUID,
        start_datetime: Optional[datetime] = Body(None),
        end_datetime: Optional[datetime] = Body(None),
        repeat_at: Optional[time] = Body(None),
        process_after: Optional[timedelta] = Body(None)
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration
    }


"""
EXTRA DATA TYPES 

Up to now, you have been using common data types, like:
- int
- float
- str
- bool

But you can also use more complex data types. And you will still have the same features as you have seen up to now:
- Great editor support
- Data conversion from incoming requests
- Data conversion for response data
- Data validation
- Automatic annotation and documentation

OTHER DATA TYPES
Here are some of the additional types you can use:

- UUID:
    - A standard "universally unique identifier", common as an ID in many databases and systems. 
    - in requests and responses, will be represented as a str.
    
- datetime.datetime:
    - A Python datetime.datetime
    - In requests and responses will be represented as a str in ISO 8601 format like: 2008-09-15T15:53:00+05:00

- datetime.date
    - Python datetime.date
    - In requests and responses will be represented as a str like 2008-09-15
    
- datetime.time
- datetime.timedelta
    - A Python datetime.timedelta
    - In requests and responses will be represented as a float of total seconds 
- frozenset
    - In requests and responses, treated the same as a `set`:
        - In requests, a list willbe read, eliminating duplicates and converting it to a set
        - In responses, the set will be converted to a list
        - The generated schema will specifiy that the set values are unique (using JSON Schema's uniqueItems)
- bytes
- Decimal
- you can check all valid Pydantic data types here: https://pydantic-docs.helpmanual.io/usage/types
"""

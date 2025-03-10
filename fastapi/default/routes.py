from fastapi import APIRouter
from typing import Union

default = APIRouter()

@default.get("/")
def read_root():
    return {"Hello": "World"}

@default.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
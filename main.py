from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from pydantic.fields import Field


app = FastAPI()


class Item(BaseModel):
    hello: Optional[str] = Field("hello", min_length=4)
    Meow: int
    d: Optional[bool] = None


@app.get("/")
async def hello_world():
    return {"message": "Hello world"}


@app.post("/")
async def post(body: Item):
    print(body)

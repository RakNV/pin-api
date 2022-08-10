from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Tag(BaseModel):
    names: list[str]


class ItemIn(BaseModel):
    img_link: str
    title: str | None
    description: str | None
    tags: Tag


class ItemOut(BaseModel):
    img_link: str
    title: str
    description: str


app = FastAPI()

db = []


@app.post("/pin", response_model=ItemOut)
async def post_pin(item: ItemIn):
    db.append(item.dict())
    return item.dict()


@app.get("/pin", response_model=list[ItemOut])
async def get_pins():
    return db


@app.delete("/pin/{item_id}", response_model=ItemOut)
async def delete_pin(item_id: int):
    if item_id > len(db) - 1:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return db[item_id]


@app.put("/pin/{item_id}", response_model=ItemOut)
async def update_pin(item_id: int, item: ItemIn):
    if item_id > len(db) - 1:
        HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item
    return db[item_id]

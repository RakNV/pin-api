from fastapi import FastAPI, HTTPException
from models import Item

app = FastAPI()

db = []


@app.post("/pin")
async def post_pin(item: Item):
    db.append(item.dict())
    return item.dict()


@app.get("/pin")
async def get_pins():
    return db


@app.delete("/pin/{item_id}")
async def delete_pin(item_id: int):
    if item_id > len(db) - 1:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return db[item_id]


@app.put("/pin/{item_id}")
async def update_pin(item_id: int, item: Item):
    if item_id > len(db) - 1:
        HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item
    return db[item_id]

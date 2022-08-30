from fastapi import FastAPI, HTTPException
from schemas import ReqModel, ResModel
from database import NotFoundError
from database import Database, DATABASE_URL

app = FastAPI()
db = Database(DATABASE_URL)


@app.post("/pin", response_model=ResModel)
async def post_pin(item: ReqModel):
    """
    Create item and store it in database
    """
    return db.create(item)


@app.get("/pin", response_model=list[ResModel])
async def get_pins():
    """
    Get all items stored in database
    """
    return db.get_all()


@app.delete("/pin/{item_id}")
async def delete_pin(item_id: int):
    """
    Deletes item by id from database
    """
    try:
        db.delete(item_id)
    except NotFoundError as e:
        print(e)
        raise HTTPException(status_code=404, detail="Not found!")


@app.put("/pin/{item_id}", response_model=ResModel)
async def update_pin(item: ReqModel, item_id: int):
    """
    Updates item in database and returns it
    """
    try:
        return db.update(item_id, item)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Not found!")

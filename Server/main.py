from fastapi import FastAPI
import db
from pydantic import BaseModel

db.init_db()
app = FastAPI()

class NewItem(BaseModel):
    name: str
    qty : int

@app.get("/menu-items")
def read_menu_items():
    return db.get_menu_items()

@app.post("/menu-items")
def add_menu_item(item: NewItem):
    db.add_menu_item(item.name)
    return {"message": f"Added {item.name} to the menu"}

@app.post("/items")
def add_item(item: NewItem):
    db.add_item(item.name, item.qty)
    return {"message": f"Added {item.name} with quantity {item.qty}"}

@app.get("/items")
def read_items():
    return db.get_items()

@app.get("/item/pending")
def get_pending_items():
    return db.get_pending_items()

@app.put("/items/{item_id}")
def update_item(item_id: int, qty: int):
    db.update_item(item_id, qty)
    return {"message": f"Updated item with ID {item_id} with quantity {qty}"}


@app.patch("/items/{item_id}/done")
def mark_item_done(item_id:int):
    db.mark_done(item_id)
    return {"message": f"Marked item with ID {item_id} as done"}

@app.delete("/items/{item_id}")
def delete_item(item_id:int):
    db.remove_item(item_id)
    return {"message": "Removed"}
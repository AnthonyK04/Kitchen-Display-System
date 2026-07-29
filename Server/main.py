from fastapi import FastAPI
import db
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from pathlib import Path
db.init_db()

app = FastAPI()

class NewItem(BaseModel):
    name: str
    qty : int
class NewMenuItem(BaseModel):
    name:str
#Menu Items
@app.get("/menu-items")
def read_menu_items():
    return db.get_menu_items()

@app.post("/menu-items")
def add_menu_item(item: NewMenuItem):
    db.add_menu_item(item.name)
    return {"message": f"Added {item.name} to the menu"}

@app.delete("/menu-items/{item_id}")
def delete_menu_item(item_id:int):
    db.remove_menu_item(item_id)
    return {"message": "Removed item from menu!"}

#Items
@app.post("/items")
def add_item(item: NewItem):
    db.add_item(item.name, item.qty)
    return {"message": f"Added {item.name} with quantity {item.qty}"}

@app.get("/items")
def read_items():
    return db.get_items()

@app.get("/items/pending")
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

public_dir = Path(__file__).parent.parent / "Frontend"
app.mount("/", StaticFiles(directory=public_dir, html=True), name="public")
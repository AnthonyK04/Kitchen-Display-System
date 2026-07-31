from fastapi import FastAPI
import db
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi import Depends
db.init_db()

app = FastAPI()

def get_db_path():
    return None

class NewItem(BaseModel):
    name: str
    qty : int
class NewMenuItem(BaseModel):
    name:str
#Menu Items
@app.get("/menu-items")
def read_menu_items(db_path: str = Depends(get_db_path)):
    return db.get_menu_items(db_path=db_path)

@app.post("/menu-items")
def add_menu_item(item: NewMenuItem,db_path: str = Depends(get_db_path)):
    db.add_menu_item(item.name,db_path=db_path)
    return {"message": f"Added {item.name} to the menu"}

@app.delete("/menu-items/{item_id}")
def delete_menu_item(item_id:int,db_path: str = Depends(get_db_path)):
    db.remove_menu_item(item_id,db_path=db_path)
    return {"message": "Removed item from menu!"}

#Items
@app.post("/items")
def add_item(item: NewItem,db_path: str = Depends(get_db_path)):
    db.add_item(item.name, item.qty,db_path=db_path)
    return {"message": f"Added {item.name} with quantity {item.qty}"}

@app.get("/items")
def read_items(db_path: str = Depends(get_db_path)):
    return db.get_items(db_path=db_path)

@app.get("/items/pending")
def get_pending_items(db_path: str = Depends(get_db_path)):
    return db.get_pending_items(db_path=db_path)

@app.put("/items/{item_id}")
def update_item(item_id: int, qty: int,db_path: str = Depends(get_db_path)):
    db.update_item(item_id, qty,db_path=db_path)
    return {"message": f"Updated item with ID {item_id} with quantity {qty}"}


@app.patch("/items/{item_id}/done")
def mark_item_done(item_id:int,db_path: str = Depends(get_db_path)):
    db.mark_done(item_id,db_path=db_path)
    return {"message": f"Marked item with ID {item_id} as done"}

@app.delete("/items/{item_id}")
def delete_item(item_id:int,db_path: str = Depends(get_db_path)):
    db.remove_item(item_id,db_path=db_path)
    return {"message": "Removed"}

public_dir = Path(__file__).parent.parent / "Frontend"
app.mount("/", StaticFiles(directory=public_dir, html=True), name="public")
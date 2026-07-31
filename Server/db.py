import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "items.db"

def get_connection(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def init_db(db_path = None):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            qty INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            cook_time INTEGER NOT NULL DEFAULT 5
        )
    """)
    conn.commit()
    conn.close()

#ITEMS TABLE 
def add_item(name, qty=0, db_path = None):
    name = name.lower()
    conn = get_connection(db_path)
    conn.execute("INSERT INTO items (name, qty) VALUES (?, ?)", (name, qty))
    conn.commit()
    conn.close()

def update_item(id, qty, db_path = None):
    conn = get_connection(db_path)
    conn.execute("UPDATE items SET qty = ? WHERE id = ?", (qty, id))
    conn.commit()
    conn.close()

def get_items(db_path = None):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_items_needed(db_path = None):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE qty > 0")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def mark_done(id, db_path = None):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET status = 'done' WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def get_pending_items(db_path=None):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE status = 'pending' ORDER BY created_at ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def remove_item(id, db_path = None):
    conn = get_connection(db_path)
    conn.execute("DELETE FROM items WHERE id = ?", (id,))
    conn.commit()
    conn.close()

#MENU_ITEMS TABLE
def add_menu_item(name, db_path = None):
    name = name.lower()
    conn = get_connection(db_path)
    conn.execute("INSERT OR IGNORE INTO menu_items (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_menu_items(db_path = None):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def remove_menu_item(id,db_path = None):
    conn = get_connection(db_path)
    conn.execute("DELETE FROM menu_items WHERE id = ?", (id,))
    conn.commit()
    conn.close()


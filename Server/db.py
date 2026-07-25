import sqlite3

def get_connection():
    return sqlite3.connect('items.db')
def init_db():
    conn = get_connection()
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
def add_item(name, qty=0):
    name = name.lower()
    conn = get_connection()
    conn.execute("INSERT INTO items (name, qty) VALUES (?, ?)", (name, qty))
    conn.commit()
    conn.close()

def update_item(id, qty):
    conn = get_connection()
    conn.execute("UPDATE items SET qty = ? WHERE id = ?", (qty, id))
    conn.commit()
    conn.close()

def get_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_items_needed():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE qty > 0")
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_done(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET status = 'done' WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def get_pending_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE status = 'pending' ORDER BY created_at ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def remove_item(id):
    conn = get_connection()
    conn.execute("DELETE FROM items WHERE id = ?", (id,))
    conn.commit()
    conn.close()

#MENU_ITEMS TABLE
def add_menu_item(name):
    name = name.lower()
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO menu_items (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_menu_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items")
    rows = cursor.fetchall()
    conn.close()
    return rows

def remove_menu_item(id):
    conn = get_connection()
    conn.execute("DELETE FROM menu_items WHERE id = ?", (id,))
    conn.commit()
    conn.close()


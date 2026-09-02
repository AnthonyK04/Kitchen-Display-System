# Kitchen Display System

A lightweight kitchen display system (KDS) for small restaurants. Front-of-house
staff send special orders to the kitchen from a tablet or phone instead of
shouting them across the line, and the kitchen works through a live queue on a
display screen. Orders can't be forgotten because they stay on the board until
someone marks them done.

## Why

In a busy kitchen, verbal orders get missed, misheard, or forgotten. This system
gives every special order a place on a screen:

- **Front of house** picks an item, sets a quantity, and hits **Send**.
- **Kitchen** sees the order appear at the bottom of a queue, cooks it, and
  presses **Enter** to clear it.
- Completed orders show briefly on the front-of-house **Done** column so the
  server knows the food is up, then auto-clear after 30 seconds.

## Architecture

```
Frontend/  (static HTML/CSS/JS, no build step)
  front.*    Front-of-house ordering screen + pending/done columns
  kitchen.*  Kitchen queue, keyboard-driven (arrow keys + Enter)
  admin.*    Menu management (add / remove menu items)

Server/  (FastAPI + SQLite)
  main.py       API routes, also serves the Frontend/ folder as static files
  db.py         SQLite access layer and schema (items.db, created on startup)
  seed_menu.py  One-off script to populate the menu with common items
  test_main.py  Integration tests (pytest + FastAPI TestClient)
```

The backend is a single FastAPI app. It exposes a small JSON API and also mounts
`Frontend/` at `/`, so one `uvicorn` process serves both the API and the UI. Data
lives in a local SQLite file (`Server/items.db`), created automatically on first
run.

### Data model

**`items`** — special orders sent to the kitchen

| column       | notes                                             |
|--------------|---------------------------------------------------|
| `id`         | primary key                                       |
| `name`       | item name, stored lowercase                       |
| `qty`        | quantity ordered                                  |
| `status`     | `pending` or `done`                               |
| `created_at` | local timestamp, used to order the kitchen queue  |

**`menu_items`** — the list of orderable items shown on the front-of-house and
admin screens

| column      | notes                          |
|-------------|--------------------------------|
| `id`        | primary key                    |
| `name`      | unique, stored lowercase       |
| `cook_time` | minutes, defaults to 5         |

## API

| Method   | Path                  | Description                                  |
|----------|-----------------------|----------------------------------------------|
| `GET`    | `/menu-items`         | List all menu items                          |
| `POST`   | `/menu-items`         | Add a menu item — body: `{ "name": str }`    |
| `DELETE` | `/menu-items/{id}`    | Remove a menu item                           |
| `GET`    | `/items`              | List all orders (pending and done)           |
| `GET`    | `/items/pending`      | List pending orders, oldest first            |
| `POST`   | `/items`              | Send an order — body: `{ "name": str, "qty": int }` |
| `PUT`    | `/items/{id}?qty=`    | Update an order's quantity                   |
| `PATCH`  | `/items/{id}/done`    | Mark an order done                           |
| `DELETE` | `/items/{id}`         | Delete an order                              |

Interactive API docs are available at `/docs` when the server is running.

## Getting started

### Prerequisites

- Python 3.11+

### Install

```bash
git clone https://github.com/AnthonyK04/Kitchen-Display-System.git
cd Kitchen-Display-System
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
cd Server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- Front of house — <http://localhost:8000/front.html>
- Kitchen display — <http://localhost:8000/kitchen.html>
- Menu admin — <http://localhost:8000/admin.html>

The frontend calls the API on port `8000` at the same hostname it's served from,
so other devices on the same network can reach it at
`http://<your-machine-ip>:8000/front.html`.

### Seed the menu (optional)

Populate `menu_items` with a starter set of common orders:

```bash
cd Server
python seed_menu.py
```

## Using the screens

**Kitchen** (`kitchen.html`) is built for a wall-mounted display and a keyboard:

- `↑` / `↓` — move the selection through the queue
- `Enter` — mark the selected order done

The queue polls every 3 seconds, and new orders drop in at the bottom.

**Front of house** (`front.html`):

- Adjust quantity with `-` / `+` or by typing, then press **Send**
- **Pending** shows orders the kitchen hasn't finished
- **Done** shows completed orders with a **Remove** button; they also clear
  automatically 30 seconds after the kitchen marks them done

**Admin** (`admin.html`) adds and removes items from the menu that front-of-house
sees.

## Tests

```bash
cd Server
pytest
```

The suite (`test_main.py`) runs against a throwaway `test_items.db` and covers the
full order lifecycle, menu management, and request validation.

## Docker

```bash
docker build -t kitchen-display-system .
docker run -p 8000:8000 kitchen-display-system
```

The container runs `uvicorn` on port 8000 and serves both the API and the
frontend. Note the SQLite database lives inside the container; mount a volume at
`/app/Server` if you need the data to persist across runs.

## Notes and limitations

- SQLite with no auth — intended for a single restaurant on a trusted local
  network, not the public internet.
- `PATCH /items/{id}/done` and `DELETE /items/{id}` return `200` even when the id
  doesn't exist.
- The frontend assumes the API is on port `8000`; if you serve it elsewhere,
  update `API_BASE` in the `Frontend/*.js` files.

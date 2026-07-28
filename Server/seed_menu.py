import db

seed_menu_items = [
    "Thigh",
    "Leg",
    "Wings",
    "Breast",
    "Fries",
    "Combo Fries",
    "Cajun Fish",
    "5pc Cajun Shrimp",
    "10pc Cajun Shrimp",
    "Steamed Dumplings",
    "Fried Dumplings"
]
db.init_db()
for item in seed_menu_items:
    db.add_menu_item(item)

print(f"Seeded {len(seed_menu_items)} menu items into the database.")
"""
generate_data.py
Genereert synthetische brondata voor het Jumbo Data Platform project.
Output: CSV-bestanden in landing_zone/sales, /products en /stores.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

# ── Reproduceerbaar ──────────────────────────────────────────────────────────
random.seed(42)

# ── Paden ────────────────────────────────────────────────────────────────────
BASE = Path(__file__).parent
LANDING = BASE / "landing_zone"

# ── Hulpfuncties ─────────────────────────────────────────────────────────────
def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  ✓ {path.relative_to(BASE)}  ({len(rows)} rijen)")


# ── 1. Stores ─────────────────────────────────────────────────────────────────
STORE_NAMES = [
    "Jumbo Amsterdam Centrum", "Jumbo Rotterdam Zuid", "Jumbo Utrecht Overvecht",
    "Jumbo Den Haag Ypenburg", "Jumbo Eindhoven Woensel", "Jumbo Groningen Noord",
    "Jumbo Tilburg Centrum", "Jumbo Almere Stad", "Jumbo Breda Centrum",
    "Jumbo Nijmegen Dukenburg",
]
FORMATS = ["Superstore", "Stadswinkel", "Buurtwinkel"]

stores = [
    {
        "store_id": f"ST{str(i+1).zfill(3)}",
        "store_name": name,
        "city": name.split()[1],
        "format": random.choice(FORMATS),
        "opening_year": random.randint(1995, 2020),
        "floor_area_m2": random.randint(400, 3500),
    }
    for i, name in enumerate(STORE_NAMES)
]


# ── 2. Products ───────────────────────────────────────────────────────────────
CATEGORIES = {
    "Zuivel": ["Melk", "Yoghurt", "Kaas", "Boter", "Kwark"],
    "Brood & Gebak": ["Witbrood", "Volkoren", "Croissant", "Muffin", "Baguette"],
    "Groente & Fruit": ["Appel", "Banaan", "Tomaat", "Sla", "Wortel"],
    "Vlees & Vis": ["Kipfilet", "Gehakt", "Zalm", "Tonijn", "Spek"],
    "Dranken": ["Cola", "Jus d'orange", "Water", "Bier", "Wijn"],
    "Snacks": ["Chips", "Noten", "Chocolade", "Koekjes", "Drop"],
}

products = []
product_id = 1
for category, items in CATEGORIES.items():
    for item in items:
        price = round(random.uniform(0.79, 8.99), 2)
        products.append({
            "product_id": f"PR{str(product_id).zfill(4)}",
            "product_name": item,
            "category": category,
            "price_eur": price,
            "is_jumbo_huismerk": random.choice([True, False]),
            "weight_gram": random.choice([100, 250, 500, 750, 1000]),
        })
        product_id += 1


# ── 3. Sales ──────────────────────────────────────────────────────────────────
START_DATE = date(2024, 1, 1)
END_DATE   = date(2024, 12, 31)
NUM_TRANSACTIONS = 5000

store_ids   = [s["store_id"]   for s in stores]
product_ids = [p["product_id"] for p in products]

sales = []
for i in range(NUM_TRANSACTIONS):
    order_date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
    quantity   = random.randint(1, 10)
    product    = random.choice(products)
    discount   = round(random.choice([0, 0, 0, 0.10, 0.15, 0.20]), 2)
    unit_price = product["price_eur"]
    revenue    = round(unit_price * quantity * (1 - discount), 2)

    sales.append({
        "transaction_id": f"TX{str(i+1).zfill(6)}",
        "order_date": order_date.isoformat(),
        "store_id": random.choice(store_ids),
        "product_id": product["product_id"],
        "quantity": quantity,
        "unit_price_eur": unit_price,
        "discount_pct": discount,
        "revenue_eur": revenue,
        "payment_method": random.choice(["pin", "pin", "pin", "cash", "app"]),
    })


# ── Wegschrijven ──────────────────────────────────────────────────────────────
print("\nGenereren van synthetische brondata...")
write_csv(LANDING / "stores"   / "stores.csv",   stores)
write_csv(LANDING / "products" / "products.csv", products)
write_csv(LANDING / "sales"    / "sales_2024.csv", sales)
print("\nKlaar! Data staat in de landing_zone/ map.")
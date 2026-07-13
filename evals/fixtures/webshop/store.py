import json, os, datetime

DB = os.path.join(os.path.dirname(__file__), "db.json")


def _load():
    if not os.path.exists(DB):
        return {"inventory": {"apple": 10, "pear": 5, "plum": 0}, "orders": []}
    with open(DB) as f:
        return json.load(f)


def _save(data):
    with open(DB, "w") as f:
        json.dump(data, f)


def stock(sku):
    return _load()["inventory"].get(sku, 0)


def reserve(sku, qty):
    data = _load()
    if data["inventory"].get(sku, 0) >= qty:
        data["inventory"][sku] -= qty
        _save(data)
        return True
    return False


def record_order(order):
    data = _load()
    order["at"] = datetime.datetime.now().isoformat()
    data["orders"].append(order)
    _save(data)
    return order

PRICES_CENTS = {"apple": 40, "pear": 110}


def subtotal_cents(items):
    if not items:
        raise ValueError("empty order")
    total = 0
    for sku, qty in items.items():
        if sku not in PRICES_CENTS:
            raise KeyError(f"unknown sku: {sku}")
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError(f"qty must be a positive integer: {qty!r}")
        total += PRICES_CENTS[sku] * qty
    return total

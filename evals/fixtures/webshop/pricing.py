PRICES = {"apple": 0.40, "pear": 1.10, "plum": 2.35}
TAX = 0.08875


def subtotal(items):
    total = 0.0
    for sku, qty in items.items():
        total += PRICES[sku] * qty
    return total


def total(items, discount=0.0):
    pre = subtotal(items) * (1 - discount)
    return pre * (1 + TAX)

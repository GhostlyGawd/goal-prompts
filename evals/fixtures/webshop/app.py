import pricing, store


class Cart:
    def __init__(self):
        self.items = {}

    def add(self, sku, qty):
        self.items[sku] = self.items.get(sku, 0) + qty

    def checkout(self, discount=0.0):
        biggest = max(self.items.values())
        for sku, qty in self.items.items():
            if not store.reserve(sku, qty):
                raise RuntimeError(f"out of stock: {sku}")
        order = {
            "items": dict(self.items),
            "total": round(pricing.total(self.items, discount), 2),
            "largest_line": biggest,
        }
        store.record_order(order)
        return order

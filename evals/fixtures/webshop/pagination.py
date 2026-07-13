def page_of(products, page, size=2):
    start = page * size
    return products[start:start + size]

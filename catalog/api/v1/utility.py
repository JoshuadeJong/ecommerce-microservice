def item2dict(item_id, item) -> dict:
    return {
        "id": item_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "stock": item.stock
    }
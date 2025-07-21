from bson import ObjectId

def product_helper(product) -> dict:
    return {
        "_id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
    }

def product_details_helper(product) -> dict:
    return {
        "name": product["name"],
        "id": str(product["_id"]),
    }

def order_helper(order, products_lookup=None) -> dict:
    # products_lookup: dict of productId -> product dict
    items = []
    total = 0.0
    for item in order["items"]:
        pid = item["productId"]
        qty = item["qty"]
        product = products_lookup[pid] if products_lookup and pid in products_lookup else None
        if product:
            items.append({
                "productDetails": product_details_helper(product),
                "qty": qty
            })
            total += product["price"] * qty
    return {
        "_id": str(order["_id"]),
        "items": items,
        "total": total,
    } 
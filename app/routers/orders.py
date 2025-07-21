from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from app.schemas import OrderCreate, OrderOut, OrderListResponse
from app.database import db
from app.models import order_helper
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    # Validate product IDs and build items
    product_ids = [ObjectId(item.productId) for item in order.items]
    products_count = await db.products.count_documents({"_id": {"$in": product_ids}})
    if products_count != len(product_ids):
        raise HTTPException(status_code=400, detail="One or more product IDs are invalid.")
    items = [{"productId": item.productId, "qty": item.qty} for item in order.items]
    order_dict = {
        "userId": order.userId,
        "items": items,
        "created_at": datetime.utcnow().isoformat(),
    }
    result = await db.orders.insert_one(order_dict)
    return {"id": str(result.inserted_id)}

@router.get("/{user_id}", response_model=OrderListResponse)
async def get_orders_for_user(
    user_id: str,
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
):
    query = {"userId": user_id}
    total_count = await db.orders.count_documents(query)
    cursor = db.orders.find(query).skip(offset).limit(limit)
    orders = []
    product_ids = set()
    orders_raw = []
    async for order in cursor:
        orders_raw.append(order)
        for item in order["items"]:
            product_ids.add(ObjectId(item["productId"]))
    # Fetch all products in one go
    products_lookup = {}
    if product_ids:
        products_cursor = db.products.find({"_id": {"$in": list(product_ids)}})
        async for product in products_cursor:
            products_lookup[str(product["_id"])] = product
    for order in orders_raw:
        orders.append(order_helper(order, products_lookup))
    page = {
        "next": offset + limit if offset + limit < total_count else None,
        "limit": len(orders),
        "previous": offset - limit if offset - limit >= 0 else None
    }
    return {"data": orders, "page": page} 
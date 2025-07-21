from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from app.schemas import ProductCreate, ProductOut, ProductListResponse
from app.database import db
from app.models import product_helper
from bson import ObjectId
import re

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    product_dict = product.dict()
    result = await db.products.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

@router.get("/", response_model=ProductListResponse)
async def list_products(
    name: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size
    total_count = await db.products.count_documents(query)
    cursor = db.products.find(query).skip(offset).limit(limit)
    products = []
    async for product in cursor:
        products.append(product_helper(product))
    # Pagination info
    page = {
        "next": offset + limit if offset + limit < total_count else None,
        "limit": len(products),
        "previous": offset - limit if offset - limit >= 0 else None
    }
    return {"data": products, "page": page} 
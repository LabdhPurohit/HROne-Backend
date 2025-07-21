from typing import List, Optional
from pydantic import BaseModel, Field

class SizeQuantity(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[SizeQuantity]

class ProductOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    price: float

    class Config:
        populate_by_name = True

class ProductListResponse(BaseModel):
    data: List[ProductOut]
    page: dict

class OrderItem(BaseModel):
    productId: str
    qty: int

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class ProductDetails(BaseModel):
    name: str
    id: str

class OrderItemOut(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderOut(BaseModel):
    id: str = Field(..., alias="_id")
    items: List[OrderItemOut]
    total: float

    class Config:
        populate_by_name = True

class OrderListResponse(BaseModel):
    data: List[OrderOut]
    page: dict 
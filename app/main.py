from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, orders

app = FastAPI()

# CORS middleware (allow all for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers will be included here after creation
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "HROne E-commerce Backend is running."} 
# HROne E-commerce Backend

This is a FastAPI backend for a simple e-commerce application, built for the HROne Backend Intern Hiring Task. It provides APIs for managing products and orders, using MongoDB as the database.

## Link
- http://35.223.135.62:8000

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Backend
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables:**
   Create a `.env` file in the root directory (`Backend/`) with your MongoDB Atlas connection string:
   ```env
   MONGODB_URI="mongodb+srv://<user>:<password>@<your-cluster-uri>"
   ```
   If you're running MongoDB locally, no `.env` file is needed.

4. **Run the app locally:**
   ```bash
   uvicorn app.main:app --reload
   ```
   The application will be running at `http://127.0.0.1:8000`.

## API Documentation

Interactive API documentation is available at `http://127.0.0.1:8000/docs` when the application is running.

## API Endpoints

### Products

#### 1. Create Product
- **POST** `/products`
- **Request Body:**
  ```json
  {
    "name": "string",
    "price": 100.0,
    "sizes": [
      {
        "size": "string",
        "quantity": 0
      }
    ]
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": "1234567890"
  }
  ```

#### 2. List Products
- **GET** `/products`
- **Query Parameters (optional):**
  - `name` (string, supports regex/partial search)
  - `size` (string, e.g., "large")
  - `limit` (integer, default: 10)
  - `offset` (integer, default: 0)
- **Response (200 OK):**
  ```json
  {
    "data": [
      {
        "id": "12345",
        "name": "Sample",
        "price": 100.0
      }
    ],
    "page": {
      "next": 10,
      "limit": 1,
      "previous": null
    }
  }
  ```

### Orders

#### 1. Create Order
- **POST** `/orders`
- **Request Body:**
  ```json
  {
    "userId": "user_1",
    "items": [
      {
        "productId": "123456789",
        "qty": 3
      }
    ]
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": "1234567890"
  }
  ```

#### 2. Get Orders for a User
- **GET** `/orders/{user_id}`
- **Query Parameters (optional):**
  - `limit` (integer, default: 10)
  - `offset` (integer, default: 0)
- **Response (200 OK):**
  ```json
  {
    "data": [
      {
        "id": "12345",
        "items": [
          {
            "productDetails": {
              "name": "Sample Product",
              "id": "123456"
            },
            "qty": 3
          }
        ],
        "total": 250.0
      }
    ],
    "page": {
      "next": 10,
      "limit": 1,
      "previous": null
    }
  }
  ```

## MongoDB Structure

### `products` Collection
```json
{
  "_id": "ObjectId('...')",
  "name": "string",
  "price": "float",
  "sizes": [
    {
      "size": "string",
      "quantity": "int"
    }
  ]
}
```

### `orders` Collection
```json
{
  "_id": "ObjectId('...')",
  "userId": "string",
  "items": [
    {
      "productId": "string",
      "qty": "int"
    }
  ],
  "created_at": "ISODate('...')"
}
```


---

**For any questions, contact the HROne team.** 

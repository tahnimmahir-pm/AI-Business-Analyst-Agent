from pymongo import MongoClient
from datetime import datetime

# MongoDB connection URI
MONGO_URI = "mongodb://root:example@localhost:27017/?authSource=admin"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["ecommerce"]

# Products data
products = [
    {
        "product_id": 1,
        "product_name": "Laptop Pro",
        "description": "High-performance laptop with 16GB RAM and 512GB SSD."
    },
    {
        "product_id": 2,
        "product_name": "Smartphone X",
        "description": "Latest smartphone with 5G support and 128GB storage."
    },
    {
        "product_id": 3,
        "product_name": "Wireless Headphones",
        "description": "Noise-cancelling headphones with 20-hour battery life."
    },
    {
        "product_id": 4,
        "product_name": "Gaming Console",
        "description": "Next-gen gaming console with 4K graphics."
    },
    {
        "product_id": 5,
        "product_name": "Smart Watch",
        "description": "Fitness tracker with heart rate monitor and GPS."
    }
]

# Sales data
sales = [
    {
        "order_id": 1,
        "product_id": 1,
        "quantity": 2,
        "unit_price": 999.99,
        "order_date": datetime(2025, 1, 15)
    },
    {
        "order_id": 2,
        "product_id": 2,
        "quantity": 5,
        "unit_price": 499.99,
        "order_date": datetime(2025, 2, 1)
    },
    {
        "order_id": 3,
        "product_id": 3,
        "quantity": 10,
        "unit_price": 99.99,
        "order_date": datetime(2025, 2, 10)
    },
    {
        "order_id": 4,
        "product_id": 4,
        "quantity": 3,
        "unit_price": 399.99,
        "order_date": datetime(2025, 3, 5)
    },
    {
        "order_id": 5,
        "product_id": 5,
        "quantity": 7,
        "unit_price": 199.99,
        "order_date": datetime(2025, 3, 20)
    },
    {
        "order_id": 6,
        "product_id": 1,
        "quantity": 1,
        "unit_price": 999.99,
        "order_date": datetime(2025, 4, 1)
    },
    {
        "order_id": 7,
        "product_id": 2,
        "quantity": 3,
        "unit_price": 499.99,
        "order_date": datetime(2025, 4, 15)
    },
    {
        "order_id": 8,
        "product_id": 3,
        "quantity": 4,
        "unit_price": 99.99,
        "order_date": datetime(2025, 5, 1)
    }
]

# Insert into collections
db.products.insert_many(products)
db.sales.insert_many(sales)

print("Data inserted successfully.")

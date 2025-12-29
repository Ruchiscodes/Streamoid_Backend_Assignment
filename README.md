# Streamoid Backend Challenge: Product Catalog Service

This repository contains my solution for the Streamoid Backend Intern/Fresher take-home exercise. I have developed a robust backend service designed to help online sellers validate and manage their product data before listing it on marketplaces.

The service is built using **FastAPI** for high-performance API handling and **SQLAlchemy** with **SQLite** for reliable data persistence.

## 🎯 Project Overview

This service streamlines the product ingestion workflow by:

* **Parsing** product catalogs from CSV files.


* **Validating** critical business rules such as price-to-MRP ratios and inventory counts.


* **Storing** valid data for quick retrieval and search through a RESTful interface.



---

## 🚀 Quick Start Guide

### Option 1: Running with Docker (Recommended)

This solution is fully dockerized to ensure it runs consistently across any environment.

1. **Build the image:**
```bash
docker build -t streamoid-catalog .

```


2. **Launch the service:**
```bash
docker run -p 8000:8000 streamoid-catalog

```



### Option 2: Running Locally

If you prefer to run the service in a local Python environment:

1. **Prepare the environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

```


2. **Install requirements:**
```bash
pip install -r requirements.txt

```


3. **Run the application:**
```bash
uvicorn app.main:app --reload

```



---

## 📖 API Endpoints & Usage

### 1. Ingest Product Data

**`POST /upload`** Accepts a CSV file to be parsed and validated. The service provides a summary of successful imports and identifies rows that failed validation.

* **Example Request:**
```bash
curl -X POST -F "file=@products1.csv" http://localhost:8000/upload

```



### 2. Retrieve Product List

**`GET /products`** Fetch all stored products. To handle large datasets efficiently, this endpoint supports pagination via `page` and `limit` parameters.

### 3. Search & Filter

**`GET /products/search`** A flexible endpoint to find products based on specific seller needs.

* **Filters Supported:** Brand, Color, and Price Range (`minPrice` to `maxPrice`) .


* **Example Request:** `GET /products/search?brand=DenimWorks&maxPrice=1500` 



---

## 🛡️ Business Validation Rules

To ensure data integrity, every uploaded row must pass the following checks:

* **Integrity:** All required fields (`sku`, `name`, `brand`, `mrp`, `price`) must be present.


* **Pricing:** The `price` must be less than or equal to the `mrp`.


* **Inventory:** The `quantity` must be a non-negative integer ().



---
## Execution & Verification Results

I have verified the implementation by running the following test cases against the local server.

1. CSV Bulk Upload & ValidationThe service successfully parsed and validated the product catalog.

**Command**: curl.exe -X POST -F "file=@products.csv" http://localhost:8000/upload 1

Output:JSON{"stored": 20, "failed": []}

Observation: All 20 items passed the integrity and business rules (Price $\le$ MRP, Quantity $\ge$ 0)

2. Product Listing with Pagination

The API efficiently handles large datasets using limit and page parameters

3.Command: curl.exe "http://localhost:8000/products?page=1&limit=2"

Output:JSON[
  {
    "sku": "TSHIRT-001",
    "name": "Cotton Tee",
    "brand": "BrandX",
    "color": "Blue",
    "size": "M",
    "mrp": 1000.0,
    "price": 800.0,
    "quantity": 10
  },
  {
    "sku": "TSHIRT-RED-001",
    "name": "Classic Cotton T-Shirt",
    "brand": "StreamThreads",
    "color": "Red",
    "size": "M",
    "mrp": 799.0,
    "price": 499.0,
    "quantity": 20
  }
]

3. Advanced Filtering (Search)

Verified that multiple filters (Brand + Price Range) can be applied simultaneously4444.

Command: curl.exe "http://localhost:8000/products/search?brand=BloomWear&maxPrice=2500" 5

[
  {"sku":"DRESS-PNK-S","name":"Floral Summer Dress","brand":"BloomWear","color":"Pink","size":"S","mrp":2499.0,"price":2199.0,"quantity":10},
  {"sku":"DRESS-YLW-M","name":"Floral Summer Dress","brand":"BloomWear","color":"Yellow","size":"M","mrp":2499.0,"price":1999.0,"quantity":7}
]
## 🧪 Quality Assurance

Quality and reliability are central to this implementation. I have included a comprehensive unit test suite to verify the CSV parser, validation logic, and search functionality.

**Run the tests:**

```bash
pytest app/tests.py

```

---

>>>>>>> 28437cd (Complete implementation: APIs, Validation, Tests, and Docker)

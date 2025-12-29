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
docker build -t streamoid-catalog 

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

##  Business Validation Rules

To ensure data integrity, every uploaded row must pass the following checks:

* **Integrity:** All required fields (`sku`, `name`, `brand`, `mrp`, `price`) must be present.


* **Pricing:** The `price` must be less than or equal to the `mrp`.


* **Inventory:** The `quantity` must be a non-negative integer ().
---

## **Execution & Verification Results**

I have rigorously verified the implementation against the local server to ensure all business logic and API requirements are met


**1. Bulk CSV Upload & Validation**

The service successfully parses product catalogs and enforces validation rules: price <= mrp, quantity >= 0, and mandatory field checks .

Command:

Bash

curl.exe -X POST -F "file=@products.csv" http://localhost:8000/upload
Response:
```
JSON

{
  "stored": 20,
  "failed": []
}

```
Observation: All 20 items passed the integrity and business rules .

**2. Product Listing with Pagination**

The API handles large datasets efficiently by using page and limit parameters.

Command:

curl.exe "http://localhost:8000/products?page=1&limit=2"

Response:
```
JSON

[
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
```

**3. Advanced Filtering**

The search endpoint supports multiple simultaneous filters: Brand, Color, and Price Range 

Command:

curl.exe "http://localhost:8000/products/search?brand=BloomWear&maxPrice=2500"


Response:
```
JSON

[
  {
    "sku": "DRESS-PNK-S",
    "name": "Floral Summer Dress",
    "brand": "BloomWear",
    "color": "Pink",
    "size": "S",
    "mrp": 2499.0,
    "price": 2199.0,
    "quantity": 10
  }
]

```
---




## Automated Testing Suite

I have implemented a comprehensive test suite using pytest to ensure code reliability and correctness of business logic.

Tests Included:

CSV Parsing: Verifies that the service correctly handles different CSV structures.

Data Validation: Confirms that rules like price <= mrp and quantity >= 0 are strictly enforced 

Search Logic: Ensures filters for brand, color, and price range return accurate subsets of data 


Run Tests:
```
pytest app/tests.py
```

## Dockerized Environment

To ensure the application runs consistently across any environment, the solution is fully containerized.


Dockerfile: Sets up the Python 3.10 environment and installs all dependencies.

Docker Compose: Orchestrates the FastAPI service and the database for easy one-command deployment.

Deployment:
```
docker-compose up --build .

```
---



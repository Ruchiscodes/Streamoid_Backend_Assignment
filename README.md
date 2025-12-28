**Streamoid Backend Challenge: Product Catalog Service**
Welcome! This repository contains my solution for the Streamoid Backend Intern/Fresher take-home exercise. I have developed a robust backend service designed to help online sellers validate and manage their product data before listing it on major marketplaces.
The service is built using FastAPI for high-performance API handling and SQLAlchemy with SQLite for reliable data persistence.

**Project Overview**
This service streamlines the product ingestion workflow by:

Parsing product catalogs from CSV files.
Validating critical business rules such as price-to-MRP ratios and inventory counts.
Storing valid data for quick retrieval and search through a RESTful interface

**Quick Start Guide**
Running with Docker
This solution is fully dockerized to ensure it runs consistently across any environment.

Build the image:
docker build -t streamoid-catalog 

Launch the service:
docker run -p 8000:8000 streamoid-catalog

**Running Locally**
If you prefer to run the service in a local Python environment:

Prepare the environment:
python -m venv venv
.\venv\Scripts\activate

Install requirements:
pip install -r requirements.txt

Run the application:
uvicorn app.main:app --reload

API Endpoints & Usage
1. Ingest Product Data
POST /upload Upload a CSV file to be parsed and validated. The service provides a summary of successful imports and identifies rows that failed validation.
Example Request:
curl -X POST -F "file=@products1.csv" http://localhost:8000/upload

2. Retrieve Product List
GET /products Fetch all stored products. To handle large datasets efficiently, this endpoint supports pagination via page and limit parameters.

3. Search & Filter
GET /products/search A flexible endpoint to find products based on specific seller needs.
Filters Supported: Brand, Color, and Price Range (minPrice to maxPrice).
Example: GET /products/search?brand=DenimWorks&maxPrice=1500

**Quality Assurance**
Quality and reliability are central to this implementation. I have included a comprehensive test suite to verify the CSV parser, validation logic, and search functionality.

Run the tests:
pytest app/tests.py


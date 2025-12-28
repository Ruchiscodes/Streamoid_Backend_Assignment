import io
import pytest
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_upload_valid_csv():
    """Test uploading a valid CSV file."""
    csv_content = (
        "sku,name,brand,color,size,mrp,price,quantity\n"
        "TSHIRT-001,Cotton Tee,BrandX,Blue,M,1000,800,10\n"
        "JEANS-002,Slim Fit,BrandY,Black,32,2000,1500,5"
    )
    files = {"file": ("products.csv", csv_content, "text/csv")}
    response = client.post("/upload", files=files)
    
    assert response.status_code == 200
    assert response.json()["stored"] == 2 
    assert len(response.json()["failed"]) == 0 

def test_validation_logic():
    """Test validation rules: Price <= MRP and Quantity >= 0."""
    csv_content = (
        "sku,name,brand,color,size,mrp,price,quantity\n"
        "FAIL-PRICE,Bad Price,BrandX,Red,L,500,600,10\n" 
        "FAIL-QTY,Bad Qty,BrandY,Blue,S,1000,800,-5\n"    
        "MISSING-FIELDS,No Name,BrandZ,Green,M,1000,,\n" 
        "VALID-001,Good Item,BrandA,White,XL,1000,900,1" 
    )
    files = {"file": ("products.csv", csv_content, "text/csv")}
    response = client.post("/upload", files=files)
    
    data = response.json()
    assert data["stored"] == 1
    assert "FAIL-PRICE" in data["failed"]
    assert "FAIL-QTY" in data["failed"]

def test_list_products_pagination():
    """Test that listing products supports limit and page."""
    response = client.get("/products?page=1&limit=1")
    assert response.status_code == 200
    assert len(response.json()) <= 1

def test_search_by_brand():
    """Test filtering by brand."""
    response = client.get("/products/search?brand=BrandA") 
    assert response.status_code == 200
    for product in response.json():
        assert "BrandA" in product["brand"]
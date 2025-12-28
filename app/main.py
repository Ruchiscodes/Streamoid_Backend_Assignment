import csv
import io
from typing import List, Optional
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session


from app import models, schemas, database
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Streamoid Product Service")

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Accepts a CSV file, validates rows, and stores valid products.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

  
    content = await file.read()
    decoded = content.decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    
    stored_count = 0
    failed_skus = []

    for row in reader:
        try:
            
            required = ["sku", "name", "brand", "mrp", "price"]
            if not all(row.get(field) for field in required):
                failed_skus.append(row.get("sku", "Missing SKU"))
                continue

          
            sku = row["sku"]
            mrp = float(row["mrp"])
            price = float(row["price"])
            quantity = int(row.get("quantity", 0))

            
            if price > mrp or quantity < 0:
                failed_skus.append(sku)
                continue

            
            db_product = models.Product(
                sku=sku,
                name=row["name"],
                brand=row["brand"],
                color=row.get("color"),
                size=row.get("size"),
                mrp=mrp,
                price=price,
                quantity=quantity
            )
           
            db.merge(db_product)
            stored_count += 1
            
        except (ValueError, KeyError):
            failed_skus.append(row.get("sku", "Invalid Data"))

    db.commit() 
    return {"stored": stored_count, "failed": failed_skus} 

@app.get("/products", response_model=List[schemas.Product])
def list_products(
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db)
):
    """
    Returns all stored products with pagination. [cite: 39-40]
    """
    skip = (page - 1) * limit
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/search", response_model=List[schemas.Product])
def search_products(
    brand: Optional[str] = None,
    color: Optional[str] = None,
    minPrice: Optional[float] = None,
    maxPrice: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    Search products by brand, color, or price range. [cite: 42-46]
    """
    query = db.query(models.Product)

    if brand:
        query = query.filter(models.Product.brand.ilike(f"%{brand}%")) 
    if color:
        query = query.filter(models.Product.color.ilike(f"%{color}%")) 
    if minPrice is not None:
        query = query.filter(models.Product.price >= minPrice)
    if maxPrice is not None:
        query = query.filter(models.Product.price <= maxPrice) 

    return query.all()
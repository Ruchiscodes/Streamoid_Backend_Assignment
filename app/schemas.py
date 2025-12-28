from pydantic import BaseModel
from typing import Optional
from pydantic import ConfigDict

class ProductBase(BaseModel):
    sku: str
    name: str
    brand: str
    color: Optional[str] = None
    size: Optional[str] = None
    mrp: float
    price: float
    quantity: int



class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
from fastapi import FastAPI, Query

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI()


# query parameters
# @app.get("/")
# def welcome_msg(name:str = "", age:int = 0):
#     return {"message": "Welcome to FAST API", "name": name, "age": age}

# query parameters
@app.get("/")
async def welcome_msg(
        name: str = Query(..., min_length=3, max_length=5), 
        age: int = Query(10, ge=1, le=100)
        ):
    
    return {
        "message": "Welcome to FAST API",
        "name"  :   name,
        "age"   :   age
    }
    
    
# path parameters
@app.get("/products/{product_sku}")
async def product_page(product_sku: str = ""):
    return {
        "message": "Welcome to Product Page",
        "product_sku"  :   product_sku,
    }
    
class Product(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, example="vijay_dev")
    email: Optional[EmailStr] = None
    phone: str
    age: Optional[int] = Field(None, ge=13, le=120, description="Age must be between 13 and 120")
    
# body parameters
@app.post("/")
async def body_page(product: Product):
    return product
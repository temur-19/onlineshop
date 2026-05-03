from pydantic import BaseModel, Field
from typing import List, Optional

class UserCreate(BaseModel):
    username: str = Field(..., max_length=100)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=100)

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    price: float

class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    user_id: int

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    product_id: int
    quantity: int
    
class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    status: str = Field(..., max_length=50)

class PaymentOut(BaseModel):
    id: int
    order_id: int
    user_id: int
    amount: float
    status: str

    class Config:
        orm_mode = True

class BalanceOut(BaseModel):
    user_id: int
    amount: float

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

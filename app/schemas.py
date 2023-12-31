from pydantic import BaseModel,EmailStr,validator
from typing import Optional
from datetime import datetime
from typing import List, Optional
import re

###########

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: str    
    

class UserCreate(UserBase):
    password: str
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        pattern = r"\(\d{3}\)-\d{3}-\d{3}"
        if not re.match(pattern, v):
            raise ValueError('Phone number must be in the format (xxx)-xxx-xxx')
        return v    

class UserDisplay(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    phone_number: Optional[str]=None    
    class Config:
        from_attributes = True
        
###########

# Seller Schemas
class SellerBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: str   

class SellerCreate(SellerBase):
    password: str
    @validator('phone_number')
    def validate_phone_number(cls, v):
        pattern = r"\(\d{3}\)-\d{3}-\d{3}"
        if not re.match(pattern, v):
            raise ValueError('Phone number must be in the format (xxx)-xxx-xxx')
        return v
    
class SellerDisplay(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

###########

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    seller_id: int

class ProductDisplay(ProductBase):
    id: int
    seller: SellerDisplay
    class Config:
        from_attributes = True
        
###########

# OrderDetail Schemas
class OrderDetailBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int

class OrderDetailCreate(BaseModel):
    product_id: int
    quantity: int
    
class OrderDetailUpdate(BaseModel):
    id: int
    quantity: Optional[int]
    product_id: int
    
class OrderDetailDisplay(OrderDetailBase):
    id: int
    product_id: Optional[int]
    class Config:
        from_attributes = True

###########

# Order Schemas
class OrderBase(BaseModel):
    user_id: int

class OrderCreate(BaseModel):
    user_id: int
    order_details: List[OrderDetailCreate]
    seller_id: int
    
class OrderUpdate(BaseModel):
    status: str 
    order_details: Optional[List[OrderDetailUpdate]]

class OrderDisplay(OrderBase):
    id: int
    created_at: datetime  
    seller: SellerDisplay
    order_details: List[OrderDetailDisplay]
    class Config:
        from_attributes = True
 
###########

# Review Schemas
class ReviewBase(BaseModel):
    content: str
    user_id: int
    product_id: int
    order_id: int  # New field
    seller_id: int  # New field

class ReviewDisplay(ReviewBase):
    id: int
    class Config:
        from_attributes = True
        
###########

# ShoppingCartItem Schemas
class ShoppingCartItemBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class ShoppingCartItemDisplay(BaseModel):
    id: int
    user_id: int
    quantity: int
    product: Optional[ProductDisplay]  # Make sure this matches the name in the SQLAlchemy model
    class Config:
        from_attributes = True
        
###########

# WishlistItem Schemas
class WishlistItemBase(BaseModel):
    user_id: int
    product_id: int

class WishlistItemDisplay(WishlistItemBase):
    id: int
    class Config:
        from_attributes = True
        
###########        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None
    
    
class Login(BaseModel):
    username: str
    password: str
from typing import List
from pydantic import BaseModel,Field,EmailStr
import datetime
from decimal import Decimal
class CreateAdvertisement(BaseModel):
    title: str = Field(
        min_length=5, 
        max_length=255,
        example="Ноутбук HP",
        description="Заголовок объявления"
    )
    description: str = Field(
        min_length=10, 
        max_length=1000,
        example="Новый ноутбук в идеальном состоянии",
        description="Подробное описание товара"
    )
    price: Decimal = Field(
        gt=0,
        example=55000.00,
        description="Цена товара"
    )
    category_id: int = Field(example=1, description="ID категории")
    
class CreateCategory(BaseModel):
    name: str = Field(
        min_length=2, 
        max_length=100,
        example="Электроника",
        description="Название категории"
    )
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id: int

class ModeratorCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRegisterCreate(BaseModel):
    username: str=Field(
        min_length=3,
        max_length=50,
        example="john_doe",
        description="Уникальное имя пользователя"
    )
    email: EmailStr = Field(
        example="user@example.com",
        description="Email пользователя"
    )
    password: str
    
class LoginRequest(BaseModel):
    username: str
    password: str
class CreateRole(BaseModel):
    name: str = Field(
        min_length=2, 
        max_length=50,
        example="admin",
        description="Название роли пользователя"
    )
class CreateResponse(BaseModel):
    message: str = Field(
        min_length=5, 
        max_length=500,
        example="Интересует товар, готов купить",
        description="Текст отклика"
    )
    advertisement_id: int = Field(
        example=1, 
        description="ID объявления"
    )

class CreateFavourite(BaseModel):
    advertisement_id: int = Field(
        example=1, 
        description="ID объявления"
    )
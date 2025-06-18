from pydantic import BaseModel,Field,EmailStr
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
class RoleBase(BaseModel):
    id: int
    name: str = Field(
        min_length=2, 
        max_length=50,
        example="admin",
        description="Название роли пользователя"
    )

class UserBase(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        example="john_doe",
        description="Уникальное имя пользователя"
    )
    email: EmailStr = Field(
        example="user@example.com",
        description="Email пользователя"
    )
    role_id: int = Field(example=1, description="ID роли пользователя")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class CategoryBase(BaseModel):
    id: int=Field(
        gt=0
    )
    name: str = Field(
        min_length=2, 
        max_length=100,
        example="Электроника",
        description="Название категории"
    )
class AdvertisementBase(BaseModel):
    title: str = Field(
        min_length=2, 
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
    
    date: datetime = Field(
        example="2023-10-15T12:30:45Z",
        description="Дата создания объявления"
    )
    created_at: datetime = Field(
        example="2023-10-15T12:30:45Z",
        description="Дата создания записи"
    )
    updated_at: datetime = Field(
        example="2023-10-15T12:30:45Z",
        description="Дата последнего обновления"
    )
    creator: Optional[UserBase] = None

class ResponseBase(BaseModel):
    message: str = Field(
        ...,
        min_length=5, 
        max_length=500,
        example="Интересует товар, готов купить",
        description="Текст отклика"
    )
    advertisement_id: int = Field(
        ..., 
        example=1, 
        description="ID объявления"
    )
    user_id: int = Field(
        ..., 
        example=1, 
        description="ID пользователя"
    )

class FavouriteBase(BaseModel):
    advertisement_id: int = Field(example=1, description="ID объявления")
    user_id: int = Field(
        ..., 
        example=1, 
        description="ID пользователя"
    )



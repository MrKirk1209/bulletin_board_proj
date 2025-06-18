from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from database import get_db
import pyd
from typing import List
import models as m
import security
router = APIRouter(prefix="/category", tags=["Category"])

@router.get("", response_model=List[pyd.CategoryBase])
def get_all_category(
    db:Session=Depends(get_db),
    page: int = Query(1, gt=0),  
    limit: int = Query(10, gt=0)): 

    category=db.query(m.Category).all()
    skip = (page - 1) * limit
    category = db.query(m.Category).offset(skip).limit(limit).all()
    return category
@router.get("/{category_id}", response_model=pyd.CategoryBase)
def get_category_by_id(category_id:int,db:Session=Depends(get_db)):
    category=db.query(m.Category).filter(
        m.Category.id==category_id
    ).first()

    if not category:
        raise HTTPException(404,"Вы ввели неправильный id")
    return category
@router.post("")
def create_category(
    category_data: pyd.CreateCategory,
    db: Session = Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin)
):
    existing_category = db.query(m.Category).filter(m.Category.name == category_data.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Указанная категория уже существует")

    new_category = m.Category(name=category_data.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
@router.put("/{category_id}")
def update_category(
    category_id: int,
    category_data: pyd.CreateCategory,
    db: Session = Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin)
):
    category = db.query(m.Category).filter(m.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    existing_category = db.query(m.Category).filter(m.Category.name == category_data.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Указанная категория уже существует")

    category.name=category_data.name
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    admin: m.User = Depends(security.require_admin),
    db: Session = Depends(get_db)
):
    category = db.query(m.Category).filter(m.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    db.delete(category)
    db.commit()
    return {"message": "Категория удалена"}
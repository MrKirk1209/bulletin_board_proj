from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from database import get_db
import pyd
from typing import List
import models as m
import security
router = APIRouter(prefix="/favourite", tags=["Favourite"])


@router.get("", response_model=List[pyd.FavouriteBase])
def get_all_favourites_user(
    db: Session = Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0)
):
    skip = (page - 1) * limit
    favourites = db.query(m.Favourite).filter(m.Favourite.user_id == current_user.id).offset(skip).limit(limit).all()
    return favourites

@router.get("/admin", response_model=List[pyd.FavouriteBase])
def get_all_favourites_admin(
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin),
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db)
):

    skip = (page - 1) * limit
    favourites = db.query(m.Favourite).offset(skip).limit(limit).all()
    return favourites

@router.get("/{favourite_id}", response_model=pyd.FavouriteBase)
def get_favourite_by_id(
    favourite_id:int,
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin),
    db:Session=Depends(get_db),
):
    favourite=db.query(m.Favourite).filter(
        m.Favourite.id==favourite_id
    ).first()

    if not favourite:
        raise HTTPException(404,"Вы ввели неправильный id")
    return favourite

@router.post("")
def create_favourite(
    favourite_data: pyd.CreateFavourite,
    db: Session = Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
):
    favourite= db.query(m.Advertisement).filter(m.Advertisement.id == favourite_data.advertisement_id).first()
    if not favourite:
        raise HTTPException(status_code=400, detail="Указана некорректное объявление")

    favourite_db=m.Favourite(user_id=current_user.id,advertisement_id=favourite_data.advertisement_id)
    db.add(favourite_db)
    db.commit()
    db.refresh(favourite_db)
    return favourite_db


@router.delete("/{favourite_id}")
def delete_favourite(
    favourite_id: int,
    current_user: pyd.UserBase = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    current_favourite = db.query(m.Favourite).filter(m.Favourite.id == favourite_id).first()
    if not current_favourite:
        raise HTTPException(status_code=404, detail="Избранное не найдено")
    if current_favourite.user_id != current_user.id and current_user.role_id not in [1, 3]:
        raise HTTPException(status_code=403, detail="Нет прав на изменение этого избранного")
    
    db.delete(current_favourite)
    db.commit()
    return {"message": "Избранное удалено"}
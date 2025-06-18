from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from database import get_db
import pyd
from typing import List
import models as m
import security
router = APIRouter(prefix="/ads", tags=["Advertisements"])

@router.get("", response_model=List[pyd.AdvertisementBase])
def get_all_ads(db:Session=Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    category: str = Query(None),
    maxPrice: float = Query(None),
    ):
    query = db.query(m.Advertisement)
    
    if category:
        category_obj = db.query(m.Category).filter(m.Category.name == category).first()
        if not category_obj:
            raise HTTPException(status_code=404, detail=f"Категория '{category}' не найдена.")
        query = query.filter(m.Advertisement.category_id == category_obj.id)

    
    if maxPrice is not None:
        query = query.filter(m.Advertisement.price <= maxPrice)

    offset = (page - 1) * limit
    ads = query.offset(offset).limit(limit).all()
    return ads

@router.get("/{ad_id}", response_model=pyd.AdvertisementBase)
def get_ad_by_id(ad_id:int,db:Session=Depends(get_db)):
    ads=db.query(m.Advertisement).filter(
        m.Advertisement.id==ad_id
    ).first()

    if not ads:
        raise HTTPException(404,"Вы ввели неправильный id")
    return ads

@router.post("/")
def create_ad(ads:pyd.CreateAdvertisement,db: Session= Depends(get_db), current_user:pyd.UserBase=Depends(security.get_current_user)):

    category = db.query(m.Category).filter(m.Category.id == ads.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Указана некорректная категория")

    ads_db=m.Advertisement(title=ads.title,description=ads.description,price=ads.price,category_id=ads.category_id,creator_id=current_user.id)
    db.add(ads_db)
    db.commit()
    db.refresh(ads_db)
    return ads_db

@router.put("/{ad_id}")
def update_ad(
    ads:pyd.CreateAdvertisement,
    ad_id:int,
    db: Session= Depends(get_db), 
    current_user:pyd.UserBase=Depends(security.get_current_user)
):
    
    ad = db.query(m.Advertisement).filter(m.Advertisement.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    category = db.query(m.Category).filter(m.Category.id == ads.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Указана некорректная категория")

    if ad.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на изменение этого объявления")
    ad.title = ads.title
    ad.description = ads.description
    ad.price = ads.price
    ad.category_id = ads.category_id

    db.commit()
    db.refresh(ad)
    return ad

@router.delete("/{ad_id}")
def delete_ad(
    ad_id: int,
    current_user: pyd.UserBase = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    ad = db.query(m.Advertisement).filter(m.Advertisement.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    if ad.creator_id != current_user.id and current_user.role_id not in [1, 3]:
        raise HTTPException(status_code=403, detail="Нет прав на изменение этого отклика")

    db.delete(ad)
    db.commit()
    return {"message": "Объявление удалено"}
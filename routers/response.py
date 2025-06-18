from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import pyd
from typing import List
import models as m
import security
router = APIRouter(prefix="/response", tags=["Response"])

from fastapi import Query
from typing import Optional

@router.get("", response_model=List[pyd.ResponseBase])
def get_all_responses(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1,),
    limit: int = Query(10, ge=1, le=10),
    user_id: Optional[int] = Query(None,),
    advertisement_id: Optional[int] = Query(None,),
):
    query = db.query(m.Response)

    if user_id is not None:
        query = query.filter(m.Response.user_id == user_id)

    if advertisement_id is not None:
        query = query.filter(m.Response.advertisement_id == advertisement_id)

    offset = (page - 1) * limit
    responses = query.offset(offset).limit(limit).all()

    return responses

@router.get("/{response_id}", response_model=pyd.ResponseBase)
def get_response_by_id(response_id:int,db:Session=Depends(get_db)):
    response=db.query(m.Response).filter(
        m.Response.id==response_id
    ).first()

    if not response:
        raise HTTPException(404,"Вы ввели неправильный id")
    return response
@router.post("")
def create_response(
    response_data: pyd.CreateResponse,
    db: Session = Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
):
    response= db.query(m.Advertisement).filter(m.Advertisement.id == response_data.advertisement_id).first()
    if not response:
        raise HTTPException(status_code=400, detail="Указана некорректное объявление")

    response_db=m.Response(message=response_data.message,user_id=current_user.id,advertisement_id=response_data.advertisement_id)
    db.add(response_db)
    db.commit()
    db.refresh(response_db)
    return response_db

@router.put("/{response_id}", response_model=pyd.ResponseBase)
def update_response(
    response_data: pyd.CreateResponse,
    response_id: int,
    db: Session = Depends(get_db), 
    current_user: pyd.UserBase = Depends(security.get_current_user)
):
    response = db.query(m.Response).filter(m.Response.id == response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Отклик не найден")

    if response.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на изменение этого отклика")
    
    ads= db.query(m.Advertisement).filter(m.Advertisement.id == response_data.advertisement_id).first()
    if not ads:
        raise HTTPException(status_code=400, detail="Указано некорректное объявление")

    response.message = response_data.message
    response.advertisement_id = response_data.advertisement_id

    db.commit()
    db.refresh(response)
    return response
@router.delete("/{response_id}")
def delete_response(
    response_id: int,
    current_user: pyd.UserBase = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    current_response = db.query(m.Response).filter(m.Response.id == response_id).first()
    if not current_response:
        raise HTTPException(status_code=404, detail="Отклик не найдена")
    
    if current_response.user_id != current_user.id and current_user.role_id not in [1, 3]:
        raise HTTPException(status_code=403, detail="Нет прав на изменение этого отклика")

    db.delete(current_response)
    db.commit()
    return {"message": "Отклик удалена"}
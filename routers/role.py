from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import pyd
from typing import List
import models as m
import security
router = APIRouter(prefix="/role", tags=["Role"])

@router.get("", response_model=List[pyd.RoleBase])
def get_all_role(
    db:Session=Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin)
):
    role=db.query(m.Role).all()
    return role
@router.get("/{role_id}", response_model=pyd.RoleBase)
def get_role_by_id(
    role_id:int,db:Session=Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin)
):
    role=db.query(m.Role).filter(
        m.Role.id==role_id
    ).first()

    if not role:
        raise HTTPException(404,"Вы ввели неправильный id")
    return role
@router.post("/")
def create_role(
    role_data: pyd.CreateRole,
    db: Session = Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin)
):
    existing_role = db.query(m.Role).filter(m.Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Указанная роль уже существует")

    existing_role = m.Role(name=role_data.name)
    db.add(existing_role)
    db.commit()
    db.refresh(existing_role)
    return existing_role
@router.put("/{role_id}")
def update_role(
    role_id: int,
    role_data: pyd.CreateRole,
    db: Session = Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin)
):
    role = db.query(m.Role).filter(m.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    
    existing_category = db.query(m.Role).filter(m.Role.name == role_data.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Указанная роль уже существует")

    role.name=role_data.name
    db.commit()
    db.refresh(role)
    return role

@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    admin: m.User = Depends(security.require_admin),
    db: Session = Depends(get_db)
):
    role = db.query(m.Role).filter(m.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    db.delete(role)
    db.commit()
    return {"message": "Категория удалена"}
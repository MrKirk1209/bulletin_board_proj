from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import pyd
from typing import List
import models as m
import security
import bcrypt 
router = APIRouter(prefix="/user", tags=["User"])

@router.get("", response_model=List[pyd.UserBase])
def get_all_user(
    db:Session=Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin)
):
    category=db.query(m.User).all()
    return category
@router.get("/{user_id}", response_model=pyd.UserBase)
def get_user_by_id(
    user_id:int,db:Session=Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin)
):
    user=db.query(m.User).filter(
        m.User.id==user_id
    ).first()

    if not user:
        raise HTTPException(404,"Вы ввели неправильный id")
    return user

@router.post("/", response_model=pyd.UserBase)
def create_user(
    user_data: pyd.UserCreate,
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin),
    db: Session = Depends(get_db)
):

    existing_user = db.query(m.User).filter(m.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    role = db.query(m.Role).filter(m.Role.id == user_data.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Указанная роль не существует")



    hashed_password = security.get_password_hash(user_data.password)
    new_user = m.User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        role_id=role.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/register", response_model=pyd.UserBase, status_code=201)
def register_user(
    user_data: pyd.UserRegisterCreate,
    db: Session = Depends(get_db)
):

    if db.query(m.User).filter(m.User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")


    if db.query(m.User).filter(m.User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")


    hashed_password = security.get_password_hash(user_data.password)
    new_user = m.User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        role_id=2 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return pyd.UserBase(
        username=new_user.username,
        email=new_user.email,
        role_id=new_user.role_id
    )

@router.put("/{user_id}")
def update_user(
    user_id: int,
    user_data: pyd.UserRegisterCreate,
    db: Session = Depends(get_db),
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin)
):
    user = db.query(m.User).filter(m.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Имя не найдено")
    
    existing_user = db.query(m.User).filter(m.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Указанное имя уже существует")
    def hash_password(plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user.username=user_data.username
    user.password=hash_password(user_data.password)
    user.email=user_data.email
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_advertisement(
    user_id: int,
    current_user: pyd.UserBase = Depends(security.get_current_user),
    admin: m.User = Depends(security.require_admin),
    db: Session = Depends(get_db)
):
    user = db.query(m.User).filter(m.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    db.delete(user)
    db.commit()
    return {"message": "Пользователь удален"}



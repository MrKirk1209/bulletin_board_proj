from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import security
import models as m
from database import get_db
from pyd.create_models import UserCreate, LoginRequest,ModeratorCreate
from pyd.base_models import UserBase, TokenResponse
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(tags=["Auth"])


from fastapi import Form

@router.post("/login", response_model=TokenResponse)
def login_user(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(m.User).filter(m.User.username == username).first()
    
    if not user or not security.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/admin/create-moderator", response_model=UserBase)
def create_moderator(
    user_data: ModeratorCreate,
    admin: m.User = Depends(security.require_admin),
    db: Session = Depends(get_db)
):
    existing_user = db.query(m.User).filter(m.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    if db.query(m.User).filter(m.User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")
    hashed_password = security.get_password_hash(user_data.password)
    new_user = m.User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        role_id=3 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



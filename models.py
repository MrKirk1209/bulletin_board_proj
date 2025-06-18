from database import Base
from sqlalchemy import Column,Integer,String,Table,ForeignKey,Float, DateTime,Numeric
from sqlalchemy.orm import relationship,Mapped
from datetime import datetime
class Advertisement(Base):
    __tablename__ = "advertisements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(255))
    price = Column(Numeric(10, 2))
    date = Column(DateTime, default=datetime.utcnow)
    

    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="advertisements")
    

    category_id = Column(Integer, ForeignKey('categorys.id'))
    category = relationship("Category", back_populates="advertisements")
    

    responses = relationship("Response", back_populates="advertisement",cascade="all, delete-orphan")
    

    favorited_by = relationship("Favourite", back_populates="advertisement")

class Category(Base):
    __tablename__ = "categorys"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    

    advertisements = relationship("Advertisement", back_populates="category")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))

    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="users")

    advertisements = relationship("Advertisement", back_populates="creator")

    responses = relationship("Response", back_populates="user")
    
    favorites = relationship("Favourite", back_populates="user")

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(255))
    

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="responses")

    advertisement_id = Column(Integer, ForeignKey('advertisements.id'))
    advertisement = relationship("Advertisement", back_populates="responses")

class Favourite(Base):
    __tablename__ = "favourites"
    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="favorites")

    advertisement_id = Column(Integer, ForeignKey('advertisements.id'))
    advertisement = relationship("Advertisement", back_populates="favorited_by")
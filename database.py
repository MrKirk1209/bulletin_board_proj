from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import func
from typing import Annotated
from datetime import datetime
engine=create_engine(f"sqlite:///./{settings.DB_NAME}.db",
                     connect_args={"check_same_thread": False} # нужно для sqlite
                     )
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)
]

class Base(DeclarativeBase):
    __abstract__ = True
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
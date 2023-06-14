from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Person(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    login = Column(String)
    password = Column(String)
    salary = Column(Integer)
    change_date = Column(Date)


SessionLocal = sessionmaker(autoflush=False, bind=engine)

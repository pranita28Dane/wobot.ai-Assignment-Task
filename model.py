from database import Base
from sqlalchemy import Column, Integer, String

class user_Model(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(String(20), nullable=False)


class todo_Model(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    description = Column(String(600), nullable=False)
    
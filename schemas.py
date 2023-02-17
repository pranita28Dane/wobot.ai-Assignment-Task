from pydantic import BaseModel
from typing import Optional

# adding a new user schema 
class user_AddSchema(BaseModel):
    username: str
    email: str
    password: str

#  user login schema
class user_Schema(BaseModel):
    email: str
    password: str

#  displaying the task schema 
class todo_DisplaySchema(BaseModel):
    id: Optional[int]
    title: str
    description: str
    
    class Config:
        orm_mode = True

# adding a new task schema for 
class todo_AddSchema(BaseModel):
    title: str
    content: str
    

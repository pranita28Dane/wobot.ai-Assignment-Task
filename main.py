from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from database import Base, SessionLocal, db_engine
from model import todo_Model, user_Model
from sqlalchemy.orm import Session
from typing import List
from schemas import todo_DisplaySchema, todo_AddSchema, user_AddSchema, user_Schema

Base.metadata.create_all(bind=db_engine)

app = FastAPI(title='To-Do List APP')


def get_db():
    DB = SessionLocal()
    try:
        yield DB
    finally:
        DB.close()

# home page
@app.get('/')
async def home():
    return "To-Do List API (FastAPI + MySQL)"


#-------------------------user operations-----------------------------------

# user signup using username, email and password
@app.post('/signup', response_class=JSONResponse)
async def signup(user:user_AddSchema, db:Session=Depends(get_db)):

    email = db.query(user_Model).filter(user_Model.email == user.email).first()
    username = db.query(user_Model).filter(user_Model.username == user.username).first()
    if email or username:
        raise HTTPException(status_code=409, detail="User is already exists")

   
    user = user_Model(username=user.username, email=user.email, password=user.password)
    db.add(user)
    db.commit()
    return "User has created successfully"

# user login using email and password
@app.post('/login', response_class=JSONResponse)
async def login(user_info:user_Schema, db:Session=Depends(get_db)):
   
    try:
        email = db.query(user_Model).filter(user_Model.email == user_info.email).first()
        password= db.query(user_Model).filter(user_Model.password == user_info.password).first()
        if email and password :
            return {"User is logged in":True}
    except:
        raise HTTPException(status_code=404, detail="wrong email or password, please try again or signup")


#-------------------------to-do list operations---------------------------------

# Create

@app.post('/add_task', response_model=todo_DisplaySchema)
async def add_tasks(todo_task:todo_AddSchema, db:Session=Depends(get_db)):
    
    todo = todo_Model(title=todo_task.title, content=todo_task.content)
    db.add(todo)
    db.commit()
    return todo

# Read
@app.get('/list_task', response_model=List[todo_DisplaySchema])
async def get_tasks(db: Session=Depends(get_db)):
    return db.query(todo_Model).all()

# Update
@app.put('/update_task/{id}', response_model=todo_DisplaySchema)
async def update_task(task_id:int, task:todo_DisplaySchema, db:Session=Depends(get_db)):
    
    try:
        update = db.query(todo_Model).filter(todo_Model.id == task_id).first()
        
        update.title=task.title
        update.content=task.content
        update.complete=task.complete
        db.add(update)
        db.commit()
        return update
   
    except:
        raise HTTPException(status_code=404, detail="task does not exist")


# Delete
@app.delete('/delete_task/{id}', response_class=JSONResponse)
async def delete_task(task_id:int, db:Session=Depends(get_db)):
   
    try:
        delete = db.query(todo_Model).filter(todo_Model.id == task_id).first()
        db.delete(delete)
        db.commit()
        return {"task of id {id} has been deleted successfully":True}
    
    except:
        return HTTPException(status_code=404, detail="task does not exist")

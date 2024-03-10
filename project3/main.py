from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, Path, status
from database import SessionLocal, engine
import models
from models import Todos
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):

    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0,lt=6)    
    complete: bool

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'Finish the thing',
                'description': 'Finish up the thing you\'ve been putting off',
                'priority': 1,
                'complete': False,
            }
        }


    
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    
    raise HTTPException(status_code=404, detail='id not found')

@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_req: TodoRequest):
    todo_model = Todos(**todo_req.model_dump())

    db.add(todo_model)
    db.commit()

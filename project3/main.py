from typing import Annotated
from fastapi import Depends, FastAPI, status
from database import SessionLocal, engine
import models
from models import Todos
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all( db: db_dependency ):
    return db.query(Todos).all()


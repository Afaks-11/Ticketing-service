import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from dotenv import load_dotenv

from .database import engine,get_db
from . import models, schemas

load_dotenv()

app = FastAPI(title="Inventory Service")

models.Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try: 
        db.execute(text('SELECT 1'))
        return { "status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.post('/events', response_model=schemas.EveentResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    new_event = models.Event(name=event.name, venue= event.venue)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    return new_event
    
# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.getenv("PORT"))
#     uvicorn.run("app:main:app", host="0.0.0.0", port=port, reload=True)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone
from typing import List

from .. import models, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix='/events', tags=['Events'])

@router.post('', response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db), _ = Depends(get_current_user)):
    if event.event_date < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail='Event date cannot be in the past.')
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event

@router.get('', response_model=List[schemas.EventResponse])
def list_events(db: Session = Depends(get_db), _ = Depends(get_current_user)):
    return db.query(models.Event).filter(models.Event.deleted_at.is_(None)).all()

@router.get('/{event_id}', response_model=schemas.EventResponse)
def get_event(event_id: UUID, db: Session = Depends(get_db), _ = Depends(get_current_user)):
    event = db.query(models.Event).filter(
        models.Event.id == event_id,
        models.Event.deleted_at.is_(None)
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found or has been deleted.")
    
    return event

@router.delete('/{event_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: UUID, db: Session = Depends(get_db), _ = Depends(get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.deleted_at.is_(None)).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    event.deleted_at = datetime.now(timezone.utc)
    db.commit()
    
    return
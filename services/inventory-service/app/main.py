import os
from uuid import UUID
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from dotenv import load_dotenv
from datetime import datetime, timezone

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
    
@app.post('/events', response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event

@app.get('/events', response_model=List[schemas.EventResponse])
def list_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@app.get('/events/{event_id}/ticket-types', response_model=List[schemas.TicketTypeResponse])
def list_ticket_types_for_events(event_id: UUID, db: Session = Depends(get_db)):
    tickets =  db.query(models.TicketType).filter(
        models.TicketType.event_id == event_id,
        models.TicketType.deleted_at.is_(None)
    ).all()
    
    if not tickets:
        raise HTTPException(status_code=404, detail='Event not found.')
    
    return tickets

@app.get('/events/{event_id}/ticket-types/{ticket_id}', response_model=schemas.TicketTypeResponse)
def get_ticket_type(event_id: UUID, ticket_id: UUID, db: Session = Depends(get_db)):
    ticket = db.query(models.TicketType).filter(
        models.TicketType.id == ticket_id,
        models.TicketType.event_id == event_id,
        models.TicketType.deleted_at.is_(None)
    ).first()
    
    if not ticket: 
        raise HTTPException(status_code=404, detail='Ticket not found.')
    
    return ticket

@app.post('/events/{event_id}/ticket-types', response_model=schemas.TicketTypeResponse)
def create_ticket_type_for_event(
    event_id: UUID, ticket_type: schemas.TicketTypeCreate, db: Session = Depends(get_db)
):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail='Event not found')
    
    existing_ticket = db.query(models.TicketType).filter(
        models.TicketType.event_id == event_id, models.TicketType.name.ilike(ticket_type.name)
    ).first()
    
    if existing_ticket: 
        raise HTTPException(
            status_code=400,
            detail=f"A ticket name '{ticket_type.name}' already existsfor this event."
        )
    
    now = datetime.now(timezone.utc)
    
    if ticket_type.sales_start_at:
        if ticket_type.sales_start_at < now:
            raise HTTPException(status_code=400, detail='Sales start date cannot be in the past.')
    
    if ticket_type.sales_end_at:
        if ticket_type.sales_end_at < now:
            raise HTTPException(status_code=400, detail='Sales end date cannot be in the past.')
        
    if ticket_type.sales_end_at and ticket_type.sales_end_at:
        if ticket_type.sales_end_at <= ticket_type.sales_start_at:
            raise HTTPException(status_code=400, detail='Sales end date must be after the start date.')
        
    db_ticket_type = models.TicketType(
        **ticket_type.model_dump(),
        event_id=event_id, 
        available_quantity=ticket_type.total_quantity, 
        sold_quantity=0,
        reserved_quantity=0
    )
    
    db.add(db_ticket_type)
    db.commit()
    db.refresh(db_ticket_type)
    
    return db_ticket_type

@app.patch('/events/{event_id}/ticket_types/{ticket_id}', response_model=schemas.TicketTypeResponse)
def update_ticket_type(
    event_id: UUID, ticket_id: UUID, ticket_update: schemas.TicketTypeUpdate, db: Session = Depends(get_db)
): 
    ticket = db.query(models.TicketType).filter(
        models.TicketType.id == ticket_id, models.TicketType.event_id == event_id, models.TicketType.deleted_at.is_(None)
    ).first()
    
    if not ticket: 
        raise HTTPException(status_code=404, detail='Ticket not found.')
    
    if ticket_update.name and ticket_update.name.lower() !=ticket.name.lower():
        existing_ticket = db.query(models.TicketType).filter(
            models.TicketType.event_id == event_id,
            models.TicketType.name.ilike(ticket_update.name),
            models.TicketType.deleted_at.is_(None)
        ).first()
        
        if existing_ticket: 
            raise HTTPException(status_code=400, detail=f"A ticket named '{ticket_update.name}' already exists.")
    
    now = datetime.now(timezone.utc)
    
    if ticket_update.sales_start_at and ticket_update.sales_start_at < now: 
        raise HTTPException(status_code=400, detail='Sales start date cannot be in the past.')
    
    if ticket_update.sales_end_at and ticket_update.sales_end_at < now:
        raise HTTPException(status_code=400, detail='Sales end date cannot be in the past.')
    
    effective_start = ticket_update.sales_start_at or ticket.sales_start_at
    effective_end = ticket_update.sales_end_at or ticket.sales_end_at
    
    if effective_start and effective_end:
        if effective_end <= effective_start:
            raise HTTPException(status_code=400, detail='Sales end date must be after the start date.')
 
    update_data = ticket_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.item():
        setattr(ticket, key, value)
        
    ticket.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ticket)
    
    return ticket

@app.delete('/events/{event_id}/ticket-types/{ticket_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket_type(event_id: UUID, ticket_id: UUID, db: Session = Depends(get_db)):
    ticket = db.query(models.TicketType).filter(
        models.TicketType.id == ticket_id,
        models.TicketType.event_id == event_id,
        models.TicketType.deleted_at.is_(None)
    ).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')
    
    ticket.deleted_at = datetime.now(timezone.utc)
    ticket.status = models.TicketStatus.DRAFT
    
    db.commit()
    return 
      
            
            
# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.getenv("PORT"))
#     uvicorn.run("app:main:app", host="0.0.0.0", port=port, reload=True)
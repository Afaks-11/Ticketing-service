from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone
from typing import List

from .. import models, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/events", tags=["Tickets"])

@router.post('/{event_id}/ticket-types', response_model=schemas.TicketTypeResponse)
def create_ticket_type_for_event(
    event_id: UUID, ticket_type: schemas.TicketTypeCreate, db: Session = Depends(get_db), _ = Depends(get_current_user)
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


@router.get('/{event_id}/ticket-types/{ticket_id}', response_model=schemas.TicketTypeResponse)
def get_ticket_type(event_id: UUID, ticket_id: UUID, db: Session = Depends(get_db),  _ = Depends(get_current_user)):
    ticket = db.query(models.TicketType).filter(
        models.TicketType.id == ticket_id,
        models.TicketType.event_id == event_id,
        models.TicketType.deleted_at.is_(None)
    ).first()
    
    if not ticket: 
        raise HTTPException(status_code=404, detail='Ticket not found.')
    
    return ticket

@router.patch('/{event_id}/ticket-types/{ticket_id}', response_model=schemas.TicketTypeResponse)
def update_ticket_type(
    event_id: UUID, ticket_id: UUID, ticket_update: schemas.TicketTypeUpdate, db: Session = Depends(get_db), _ = Depends(get_current_user)
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
    
    for key, value in update_data.items():
        setattr(ticket, key, value)
        
    ticket.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ticket)
    
    return ticket

@router.delete('/{event_id}/ticket-types/{ticket_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket_type(event_id: UUID, ticket_id: UUID, db: Session = Depends(get_db), _ = Depends(get_current_user)):
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

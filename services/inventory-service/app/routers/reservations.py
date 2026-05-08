from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone, timedelta
from typing import List

from .. import models, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post('', response_model=schemas.ReservationResponse)    
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ticket = db.query(models.TicketType).filter(
        models.TicketType.id == reservation.ticket_type_id,
        models.TicketType.deleted_at.is_(None)
    ).first()       
    
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket Type not found')

    if ticket.available_quantity < reservation.quantity:
        raise HTTPException(status_code=400, detail='Not enough tickets available')  
    
    ticket.available_quantity -= reservation.quantity
    ticket.reserved_quantity += reservation.quantity
    
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=5)   
    
    db_reservation = models.Reservation(
        ticket_type_id = reservation.ticket_type_id,
        user_id= current_user['id'],
        quantity= reservation.quantity,
        status = models.ReservationStatus.ACTIVE,
        expires_at = expiration_time
    )       
    
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    
    return db_reservation


@router.get('/{reservation_id}', response_model=schemas.ReservationResponse)
def get_reservation(reservation_id: UUID, db: Session = Depends(get_db),  current_user: dict = Depends(get_current_user)): 
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id, models.Reservation.user_id == current_user['id']).first()
    if not reservation:
        raise HTTPException(status_code=404, detail='Reservation not found.')
    return reservation

@router.patch('/{reservation_id}', response_model=schemas.ReservationResponse)
def extend_reservation(reservation_id: UUID, req: schemas.ReservationUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id, models.Reservation.user_id == current_user['id']).first()
    
    if not reservation: 
        raise HTTPException(status_code=404, detail='Reservation not found.')
    
    if reservation.status != models.ReservationStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Can only extend ACTIVE reservations.")
    
    if req.expires_at <= datetime.now(timezone.utc): 
        raise HTTPException(status_code=400, detail='New expiration time must be in the future.')
    
    reservation.expires_at = req.expires_at
    
    db.commit()
    db.refresh(reservation)
    
    return reservation

@router.delete('/{reservation_id}', status_code=status.HTTP_204_NO_CONTENT)
def cancel_reservation(reservation_id: UUID, db: Session = Depends(get_db),  current_user: dict = Depends(get_current_user)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id, models.Reservation.user_id == current_user['id']).first()
    
    if not reservation: 
        raise HTTPException(status_code=404, detail='Reservation not found.')
    
    if reservation.status != models.ReservationStatus.ACTIVE:
        raise HTTPException(status_code=400, detail='Reservation is already expired or converted.')
    
    ticket = db.query(models.TicketType).filter(models.TicketType.id == reservation.ticket_type_id).first()
    
    if ticket: 
        ticket.available_quantity += reservation.quantity
        ticket.reserved_quantity -= reservation.quantity
        
    reservation.status = models.ReservationStatus.EXPIRED
    
    db.commit()
    return 

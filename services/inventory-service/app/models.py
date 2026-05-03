import uuid
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from .database import Base

class TicketStatus(str, enum.Enum):
    DRAFT = 'draft'
    ACTIVATE = 'activate'
    SOLD_OUT = 'sold_out'
    PAUSED = "paused"
    
class ReservationStatus(str, enum.Enum):
    ACTIVE = 'active'
    EXPIRED = 'expired'
    CONVERTED= 'converted'

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    
    ticket_type = relationship('TicketType', back_populates='event', cascade='all, delete-orphan')
    
class TicketType(Base): 
    __tablename__ = 'ticket_types'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    total_quantity = Column(Integer, nullable=False)
    available_quantity = Column(Integer, nullable=False)
    reserved_quantity = Column(Integer, default=0)
    sold_quantity  = Column(Integer, default=0)
    refunded_quantity = Column(Integer, default=0)
    
    price = Column(Float, nullable=False)
    currency = Column(String, default='Naira')
    dynamic_pricing_rules = Column(JSON, nullable=True)
    discount_id = Column(UUID(as_uuid=True), nullable=True)
    
    age_restriction = Column(Integer, nullable=True)
    
    sales_start_at = Column(DateTime, nullable=True)
    sales_end_at = Column(DateTime, nullable=True)
    
    status = Column(Enum(TicketStatus), default=TicketStatus.DRAFT)
    is_hidden = Column(Boolean, default=False)
    sales_channel = Column(String, nullable=True)
    
    is_seated = Column(Boolean, default=False)
    seat_map_id = Column(UUID(as_uuid=True), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1) # Optimistic locking!
    deleted_at = Column(DateTime, nullable=True)
    
    event = relationship("Event", back_populates="ticket_types")
    reservations = relationship("Reservation", back_populates="ticket_type")
    
class Reservation(Base): 
    __tablename__ = 'reservations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    ticket_type_id = Column(UUID(as_uuid=True), ForeignKey("ticket_types.id"), nullable=False)
    
    user_id = Column(String, nullable=True) 
    
    quantity = Column(Integer, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.ACTIVE)
    
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    ticket_type = relationship("TicketType", back_populates="reservations")
import uuid
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class TicketStatus(str, enum.Enum):
    DRAFT = 'draft'
    ACTIVE = 'active'
    SOLD_OUT = 'sold_out'
    PAUSED = "paused"

class TicketType(Base): 
    __tablename__ = 'ticket_types'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), nullable=False)
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
    
    age_restriction = Column(Integer, nullable=False)
    
    sales_start_at = Column(DateTime, nullable=True)
    sales_end_at = Column(DateTime, nullable=True)
    
    status = Column(Enum(TicketStatus, values_callable=lambda obj: [e.value for e in obj]), default=TicketStatus.DRAFT)
    is_hidden = Column(Boolean, default=False)
    sales_channel = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1) # Optimistic locking!
    deleted_at = Column(DateTime, nullable=True)
    
    # Use strings for relationships
    event = relationship("Event", back_populates="ticket_types")
    reservations = relationship("Reservation", back_populates="ticket_type")
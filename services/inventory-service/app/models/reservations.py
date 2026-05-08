import uuid
import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class ReservationStatus(str, enum.Enum):
    ACTIVE = 'active'
    EXPIRED = 'expired'
    CONVERTED = 'converted'

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
from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional
from ..models.reservations import ReservationStatus

class ReservationBase(BaseModel): 
    ticket_type_id: UUID4
    user_id: Optional[str] = None
    quantity: int = Field(..., gt=0, description='Number of tickets to hold')
    
class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    expires_at: datetime
    
class ReservationResponse(ReservationBase): 
    id: UUID4
    status: ReservationStatus
    expires_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
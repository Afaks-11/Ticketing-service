from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import List
from .tickets import TicketTypeResponse # Import ticket response for the nested list

class EventBase(BaseModel):
    name: str
    venue: str
    event_date: datetime

class EventCreate(EventBase):
    pass
   
class EventResponse(EventBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    ticket_types: List[TicketTypeResponse] = []
    
    class Config:
        from_attributes = True
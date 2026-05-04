from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import List, Optional, Dict, Any

from .models import TicketStatus

class TicketTypeBase(BaseModel):
    name: str
    description:str
    
    #Capacity & Pricing
    total_quantity: int = Field(..., gt=0)
    price: float = Field(..., ge=0)
    currency: Optional[str] = "Naira"
    
    dynamic_pricing_rules: Optional[Dict[str, Any]] = None
    sales_start_at: Optional[datetime] = None
    sales_end_at: Optional[datetime]= None
    status: Optional[TicketStatus] = TicketStatus.DRAFT
    is_hidden: Optional[bool] = False
    sales_channel: Optional[str] = None
    age_restriction: int = Field(default=0, ge=0)
    
class TicketTypeCreate(TicketTypeBase):
    # We will grab that from the URL path (e.g., POST /events/{event_id}/tickets)
    pass

class TicketTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    total_quantity: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = None
    dynamic_pricing_rules: Optional[Dict[str, Any]] = None
    discount_id: Optional[UUID4] = None
    sales_start_at: Optional[datetime] = None
    sales_end_at: Optional[datetime] = None
    status: Optional[TicketStatus] = None
    is_hidden: Optional[bool] = None
    sales_channel: Optional[str] = None
    age_restriction: Optional[int] = Field(None, ge=0)

class TicketTypeResponse(TicketTypeBase):
    id: UUID4
    event_id: UUID4
    
    available_quantity: int
    reserved_quantity: int
    sold_quantity: int
    refunded_quantity: int
    
    created_at: datetime
    updated_at: datetime
    version: int
    
    class Config:
        from_attributes = True
        
        
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
        # This tells Pydantic to read data even if it's not a standard dictionary
        # (Crucial for reading directly from SQLAlchemy database models)
        from_attributes = True
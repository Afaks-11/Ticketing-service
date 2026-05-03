from pydantic import BaseModel
from datetime import datetime
from typing import List

class EventCreate(BaseModel):
    name: str
    venue: str
    
class EveentResponse(BaseModel):
    id: int
    name: str
    venue: str
    date: datetime
    
    class config:
        # This tells Pydantic to read data even if it's not a standard dictionary
        # (Crucial for reading directly from SQLAlchemy database models)
        from_attributes = True
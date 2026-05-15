from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CheckoutRequest(BaseModel):
    order_id: UUID
    
class CheckoutResponse(BaseModel):
    checkout_url: str
    transaction_id: UUID
    
class TransactionUpdate(BaseModel):
    status: str
    stripe_checkout_id: Optional[str] = None
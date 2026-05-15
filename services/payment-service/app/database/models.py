import enum
import uuid
from sqlalchemy import Column, String, Float, Enum, DateTime, text 
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .database import Base

class TransactionStatus(str, enum.Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    REFUNDED = 'REFUNDED'
    
class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), nullable=False)
    
    stripe_checkout_id = Column(String, unique=True, nullable=True)
    
    amount = Column(Float, nullable=False)
    currency = Column(String, default='NGN')
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
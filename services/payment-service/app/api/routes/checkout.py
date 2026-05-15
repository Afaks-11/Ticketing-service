from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.database.models import Transaction, TransactionStatus
from app.schemas.payment import CheckoutRequest, CheckoutResponse
from app.services.order_svc import get_order_details
from app.services.stripe_svc import create_stripe_checkout_session


router = APIRouter()

@router.post('/checkout', response_model=CheckoutResponse)
async def create_checkout( payload: CheckoutRequest, authorization: str = Header(None), db: AsyncSession = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization header missing')
    
    order = await get_order_details(str(payload.order_id), authorization)
    
    if order['status'] != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order is in {order['status']} status and cannont be paid."
        )
        
    try: 
        stripe_session = await create_stripe_checkout_session(
            order_id= str(payload.order_id),
            amount=order['totalAmount']
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    new_transaction = Transaction(
        order_id=payload.order_id,
        stripe_checkout_id = stripe_session.id,
        amount=order['totalAmount'],
        status= TransactionStatus.PENDING
    )
    
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    
    return {
        "checkout_url": stripe_session.url,
        "transaction_id": new_transaction.id
    }
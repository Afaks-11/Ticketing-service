import httpx
from fastapi import HTTPException, status
from app.core.config import settings

async def get_order_details(order_id: str, auth_header: str):
    """
    Fetches order details from the Order Service to verify price and status.
    We pass the auth_header to act on behalf of the user.
    """
    
    async with httpx.AsyncClient() as client: 
        try:
            response = await client.get(
                f"{settings.ORDER_SERVICE_URL}/orders/{order_id}", 
                headers={'Authorization': auth_header})

            if response.status_code != 200: 
                raise HTTPException(
                    status_code=response.status_code, detail='Could not verify order with Order Service.'
                )
                
            return response.json()
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail='Order Service is currently unreachable'
            )
    
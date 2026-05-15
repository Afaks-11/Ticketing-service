import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

async def create_stripe_checkout_session(order_id: str, amount: float, currency: str = 'NGN'):
    """
    Creates a Stripe Checkout Session and returns the URL.
    """
    try: 
        # Stripe expects integers in the smallest currency unit (kobo)
        unit_amount = int(round(float(amount) * 100))
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency, 
                    'product_data': {
                        'name': f"Order #{order_id}"
                    }, 
                    'unit_amount': unit_amount               
                },
                'quantity':1
            }],
            mode='payment',
            metadata={
                'order_id': order_id
            }
        )
        return session
    except Exception as e:
        raise Exception(f"Stripe Session Error: {str(e)}")
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(product, success_url, cancel_url, buyer_email):
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=buyer_email,
            payment_method_types=['card'],
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': product.title}, 'unit_amount': int(product.price * 100)}, 'quantity': 1}],
            mode='payment',
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
            metadata={'product_id': product.id}
        )
        return checkout_session.id, checkout_session.url
    except Exception:
        return None, None

def verify_checkout_session(session_id):
    try:
        return stripe.checkout.Session.retrieve(session_id)
    except Exception:
        return None

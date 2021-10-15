

import stripe
from .. import keys

stripe.api_key = keys.payments.test

#-----------------------------------------------------
# Capture a stripe payment intent
#
# Parms:
#   product_request_session_id: the session_id that belongs to the product request
#
# Returns a stripe Payment intent
# ----------------------------------------------------
def capturePayment(product_request_session_id) -> stripe.PaymentIntent:
    return _handlePayment(product_request_session_id, True)


def cancelPayment(product_request_session_id) -> stripe.PaymentIntent:
    return _handlePayment(product_request_session_id, False)

def _handlePayment(product_request_session_id, capture: bool):
    session = stripe.checkout.Session.retrieve(product_request_session_id)
    
    if capture:
        intent = stripe.PaymentIntent.capture(session.payment_intent)
    else:
        intent = stripe.PaymentIntent.cancel(session.payment_intent)

    return intent
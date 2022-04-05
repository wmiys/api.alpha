import stripe
from wmiys_common import keys
from wmiys_common import utilities
from api_wmiys.common.base_return import BaseReturn

from api_wmiys.domain import models

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

#-----------------------------------------------------
# Cancel a stripe payment intent
#
# Parms:
#   product_request_session_id: the session_id that belongs to the product request
#
# Returns a stripe Payment intent
# ----------------------------------------------------
def cancelPayment(product_request_session_id) -> stripe.PaymentIntent:
    return _handlePayment(product_request_session_id, False)

#-----------------------------------------------------
# Internal function for either capturing or canceling a payment intent
# ----------------------------------------------------
def _handlePayment(product_request_session_id, capture: bool):
    session = stripe.checkout.Session.retrieve(product_request_session_id)
    
    if capture:
        intent = stripe.PaymentIntent.capture(session.payment_intent)
    else:
        intent = stripe.PaymentIntent.cancel(session.payment_intent)

    return intent


#------------------------------------------------------
# Create a new stripe account
#------------------------------------------------------
def createNewStripeAccount(user_id: int) -> stripe.Account:
    return stripe.Account.create(
        type     = 'express',
        metadata = dict(user_id=user_id)
    )



#------------------------------------------------------
# Tell stripe to send a lender their current balance
# 
# Returns a BaseReturn:
#   - the data value is set to the resulting stripe.Transfer object
#------------------------------------------------------
def sendBalanceTransfer(balance_transfer: models.BalanceTransfer) -> BaseReturn:
    result = BaseReturn(successful=True)

    try:
        stripe_transfer: stripe.Transfer = stripe.Transfer.create(
            amount      = utilities.dollarsToCents(balance_transfer.amount),
            currency    = "usd",
            destination = balance_transfer.destination_account_id,
            metadata    = dict(balance_transfer_id=str(balance_transfer.id))
        )

        result.data = stripe_transfer
    
    except Exception as e:
        result.successful = False
        result.error      = e
        result.data       = None

    return result



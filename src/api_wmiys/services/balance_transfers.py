"""
**********************************************************************************************

Balance transfers occur when a lender wants to transfer their earnings to their bank account.
Lenders need to have a balance greater than 1 in order to successfully transfer their balance.

**********************************************************************************************
"""
from __future__ import annotations
from datetime import datetime
import flask

import stripe

from wmiys_common import utilities
from api_wmiys.services import users as user_services
from api_wmiys.common import responses
from api_wmiys.domain import models
from api_wmiys import payments



#------------------------------------------------------
# Create a new balance transfer
#------------------------------------------------------
def responses_POST() -> flask.Response:
    # make sure user has a balance greater than 1 before sending it
    balance_transfer = _createNewModel()

    # check to make sure the user has a stripe account on file and they have sufficient funds
    if not balance_transfer.destination_account_id:
        return responses.badRequest('Stripe account is not setup.')
    elif balance_transfer.amount < 1:
        return responses.badRequest('Insufficient funds')

    # send their balance to them using stripe
    try:
        balance_transfer.transfer_id = _sendTransfer(balance_transfer)
    except Exception as e:
        return responses.badRequest(str(e))

    
    # record the transfer in the database


    return responses.created(balance_transfer)



#------------------------------------------------------
# Create a new BalanceTransfer model
#------------------------------------------------------
def _createNewModel() -> models.BalanceTransfer:
    user_stats = _getUserStats()
    
    balance_transfer = models.BalanceTransfer(
        id                     = utilities.getUUID(False),
        user_id                = flask.g.client_id,
        amount                 = user_stats.get('lender_balance') or 0,
        destination_account_id = user_stats.get('payout_account_id'),
        created_on             = datetime.now()
    )

    return balance_transfer


#------------------------------------------------------
# Get the user's data
#------------------------------------------------------
def _getUserStats() -> dict:
    return user_services.getUserView(flask.g.client_id)


#------------------------------------------------------
# Send the BalanceTransfer to Stripe and transfer the amount
# Returns the stripe.Transfer id
#------------------------------------------------------
def _sendTransfer(balance_transfer: models.BalanceTransfer) -> str:
    result = payments.sendBalanceTransfer(balance_transfer)

    if not result.successful:
        raise result.error

    return result.id


        



"""
**********************************************************************************************

Balance transfers occur when a lender wants to transfer their earnings to their bank account.
Lenders need to have a balance greater than 1 in order to successfully transfer their balance.

**********************************************************************************************
"""

from __future__ import annotations
from datetime import datetime
import flask

from wmiys_common import utilities
from api_wmiys import payments
from api_wmiys.common import responses
from api_wmiys.domain import models
from api_wmiys.repository import balance_transfers as balance_transfers_repo
from api_wmiys.services import users as user_services


#------------------------------------------------------
# Create a new balance transfer
#------------------------------------------------------
def responses_POST() -> flask.Response:
    balance_transfer = _createNewModel()

    try:
        # validate the model before anything else
        _validateModel(balance_transfer)

        # send the user's funds to them using stripe
        balance_transfer.transfer_id = _sendTransfer(balance_transfer)

        # record the transfer in the database
        _saveTransferToDatabase(balance_transfer)
    
    except Exception as e:
        return responses.badRequest(str(e))

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
# Validate the given BalanceTransfer:
#   - client has a stripe account set up
#   - client has a lender balance greater than 1
#------------------------------------------------------
def _validateModel(balance_transfer: models.BalanceTransfer):
    if not balance_transfer.destination_account_id:
        raise Exception('Stripe account is not setup.')
    elif balance_transfer.amount < 1:
        raise Exception('Insufficient funds')


#------------------------------------------------------
# Send the BalanceTransfer to Stripe and transfer the amount
# Returns the stripe.Transfer id
#------------------------------------------------------
def _sendTransfer(balance_transfer: models.BalanceTransfer) -> str:
    result = payments.sendBalanceTransfer(balance_transfer)

    if not result.successful:
        raise result.error

    return result.data.id

#------------------------------------------------------
# Record the given BalanceTransfer object in the database
#------------------------------------------------------
def _saveTransferToDatabase(balance_transfer: models.BalanceTransfer) -> bool:
    db_result = balance_transfers_repo.insert(balance_transfer)

    if not db_result.successful:
        raise db_result.error

    return True

        



"""
Package:        balance_transfers
Url Prefix:     /balance-transfers
Description:    Routing for balance transfers
"""

from http import HTTPStatus

import flask

from wmiys_common import utilities
from api_wmiys.common import security
from api_wmiys.models import BalanceTransfer

from api_wmiys.services import balance_transfers as balance_transfer_services
# from api_wmiys.services import users as user_services


bp_balance_transfers = flask.Blueprint('bp_balance_transfers', __name__)


#------------------------------------------------------
# Create a new balance transfer
#------------------------------------------------------
@bp_balance_transfers.post('')
@security.login_required
def post():

    return balance_transfer_services.responses_POST()


    # make sure that the lender has a balance greater than 1
    user_stats = user_services.getUserView(flask.g.client_id)

    if user_stats.get('lender_balance', 0) < 1:
        return ('Insufficient funds', HTTPStatus.BAD_REQUEST.value)

    # create a new balance transfer object
    transfer = BalanceTransfer(
        id                     = utilities.getUUID(False),              # generate a new UUID
        user_id                = flask.g.client_id,
        amount                 = user_stats.get('lender_balance', 0),
        destination_account_id = user_stats.get('payout_account_id'),
    )
    
    # try to transfer the balance on stripe
    if not transfer.sendTransfer():
        return ('Error sending transfer to stripe.', HTTPStatus.BAD_REQUEST.value)

    # insert the transfer record into the database
    transfer.insert()

    return flask.jsonify(transfer.__dict__)

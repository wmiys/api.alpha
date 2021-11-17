"""
Package:        balance_transfers
Url Prefix:     /balance-transfers
Description:    Routing for balance transfers

"""

import flask
from wmiys_common import utilities
from ..common import security
from ..models import BalanceTransfer, User
from http import HTTPStatus

bp_balance_transfers = flask.Blueprint('bp_balance_transfers', __name__)


#------------------------------------------------------
# Create a new balance transfer
#------------------------------------------------------
@bp_balance_transfers.post('')
@security.login_required
def post():
    # make sure that the lender has a balance greater than 1
    user = User(id=security.requestGlobals.client_id)
    user_stats = user.get()

    if user_stats.get('lender_balance', 0) < 1:
        return ('Insufficient funds', HTTPStatus.BAD_REQUEST.value)

    # create a new balance transfer object
    transfer = BalanceTransfer(
        id                     = utilities.getUUID(False),              # generate a new UUID
        user_id                = security.requestGlobals.client_id,
        amount                 = user_stats.get('lender_balance', 0),
        destination_account_id = user_stats.get('payout_account_id'),
    )
    
    # try to transfer the balance on stripe
    if not transfer.sendTransfer():
        return ('Error sending transfer to stripe.', HTTPStatus.BAD_REQUEST.value)

    # insert the transfer record into the database
    transfer.insert()

    return flask.jsonify(transfer.__dict__)

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
    user = User(id=security.requestGlobals.client_id)
    user_stats = user.get()

    if user_stats.get('lender_balance', 0) < 1:
        return ('Insufficient funds', HTTPStatus.BAD_REQUEST.value)

    transfer = BalanceTransfer(
        id                     = utilities.getUUID(False),
        user_id                = security.requestGlobals.client_id,
        amount                 = user_stats.get('lender_balance', 0),
        destination_account_id = user_stats.get('payout_account_id'),
    )
    
    if not transfer.sendTransfer():
        return ('Error sending transfer to stripe.', HTTPStatus.BAD_REQUEST.value)

    transfer.insert()

    return flask.jsonify(transfer.__dict__)

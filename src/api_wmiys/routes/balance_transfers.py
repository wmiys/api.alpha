"""
Package:        balance_transfers
Url Prefix:     /balance-transfers
Description:    Routing for balance transfers
"""

import flask
from api_wmiys.common import security
from api_wmiys.services import balance_transfers as balance_transfer_services

bp_balance_transfers = flask.Blueprint('bp_balance_transfers', __name__)

#------------------------------------------------------
# Create a new balance transfer
#------------------------------------------------------
@bp_balance_transfers.post('')
@security.login_required
def post():
    return balance_transfer_services.responses_POST()

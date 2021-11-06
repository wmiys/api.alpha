"""
Package:        payout_accounts
Url Prefix:     /payout-accounts/
Description:    Routing for creating payout accounts

This is not accessible to any 3rd party clients.
Only accessible by the front-end.
"""

import flask
from wmiys_common import utilities
from ..common import security
from ..models import Payment
from http import HTTPStatus

bp_payout_accounts = flask.Blueprint('bp_payout_accounts', __name__)


#------------------------------------------------------
# Create a new payout account
#------------------------------------------------------
@bp_payout_accounts.post('')
@security.no_external_requests
@security.login_required
def post():
    return 'create new payout account'

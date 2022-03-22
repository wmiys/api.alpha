"""

Package:        payout_accounts
Url Prefix:     /payout-accounts/
Description:    Routing for creating payout accounts

This is not accessible to any 3rd party clients.
Only accessible by the front-end.

"""

import uuid
import flask
from api_wmiys.common import security
from api_wmiys.services import payout_accounts as payout_account_services

bp_payout_accounts = flask.Blueprint('bp_payout_accounts', __name__)

#------------------------------------------------------
# Create a new payout account
#------------------------------------------------------
@bp_payout_accounts.post('')
@security.no_external_requests
@security.login_required
def post():
    return payout_account_services.response_POST()

#------------------------------------------------------
# Get all payout accounts owned by the user
#------------------------------------------------------
@bp_payout_accounts.get('')
@security.no_external_requests
@security.login_required
def getAll():
    return payout_account_services.response_GET_ALL()

#------------------------------------------------------
# Get a single payout account 
#------------------------------------------------------
@bp_payout_accounts.get('<uuid:payout_account_id>')
@security.no_external_requests
@security.login_required
def get(payout_account_id: uuid.UUID):
    return payout_account_services.response_GET(payout_account_id)


#------------------------------------------------------
# Update a record
#------------------------------------------------------
@bp_payout_accounts.put('<uuid:payout_account_id>')
@security.no_external_requests
@security.login_required
def put(payout_account_id: uuid.UUID):
    return payout_account_services.response_PUT(payout_account_id)

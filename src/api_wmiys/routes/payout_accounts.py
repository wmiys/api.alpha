"""
Package:        payout_accounts
Url Prefix:     /payout-accounts/
Description:    Routing for creating payout accounts

This is not accessible to any 3rd party clients.
Only accessible by the front-end.
"""
import uuid
import flask
from wmiys_common import utilities
from ..common import security
from ..models import PayoutAccount, payout_account
from http import HTTPStatus

bp_payout_accounts = flask.Blueprint('bp_payout_accounts', __name__)


#------------------------------------------------------
# Create a new payout account
#------------------------------------------------------
@bp_payout_accounts.post('')
@security.no_external_requests
@security.login_required
def post():
    new_stripe_account = payout_account.getNewStripeAccount()

    account = PayoutAccount(
        id         = utilities.getUUID(False),
        user_id    = security.requestGlobals.client_id,
        account_id = new_stripe_account.stripe_id
    )

    if not account.insert():
        return ('Did not insert!', HTTPStatus.BAD_REQUEST.value)
    
    return flask.jsonify(account.__dict__)


#------------------------------------------------------
# Get all payout accounts owned by the user
#------------------------------------------------------
@bp_payout_accounts.get('')
@security.no_external_requests
@security.login_required
def getAll():
    accounts = payout_account.getAll(security.requestGlobals.client_id)
    return flask.jsonify(accounts)
    

#------------------------------------------------------
# Get a single payout account 
#------------------------------------------------------
@bp_payout_accounts.get('<uuid:payout_account_id>')
@security.no_external_requests
@security.login_required
def get(payout_account_id: uuid.UUID):
    account = PayoutAccount(
        id      = payout_account_id,
        user_id = security.requestGlobals.client_id
    )
    
    return flask.jsonify(account.get())

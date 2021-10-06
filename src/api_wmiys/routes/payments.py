"""
Package:        payments
Url Prefix:     /payments/
Description:    Routing for locations
"""

import flask
from ..common import security

bp_payments = flask.Blueprint('bp_payments', __name__)


#------------------------------------------------------
# Create a new payment route
#------------------------------------------------------
@bp_payments.route('', methods=['POST'])
@security.login_required
def getLocations():

    data = flask.request.form.to_dict()
    print(flask.json.dumps(data, indent=4))

    return 'payments resource'
"""
Package:        payments
Url Prefix:     /payments/
Description:    Routing for payments
"""

import flask
from api_wmiys.common import security
from api_wmiys.services import payments as payment_services

bp_payments = flask.Blueprint('bp_payments', __name__)

#------------------------------------------------------
# Create a new payment record
#------------------------------------------------------
@bp_payments.post('')
@security.no_external_requests
@security.login_required
def insertPayment():
    return payment_services.responses_POST()

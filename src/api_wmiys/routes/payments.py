"""
Package:        payments
Url Prefix:     /payments/
Description:    Routing for locations


Required form fields:
    - ends_on
    - location_id
    - product_id
    - starts_on

"""

import flask
from ..common import security, utilities
from ..models import Payment
from http import HTTPStatus

bp_payments = flask.Blueprint('bp_payments', __name__)


#------------------------------------------------------
# Create a new payment route
#------------------------------------------------------
@bp_payments.route('', methods=['POST'])
@security.no_external_requests
@security.login_required
def insertPayment():
    
    payment = Payment(
        id        = utilities.getUUID(True),
        renter_id = security.requestGlobals.client_id,
    )

    # set the object's property values from the request form data
    request_data = flask.request.form.to_dict()

    if utilities.areAllKeysValidProperties(request_data, payment):
        utilities.setPropertyValuesFromDict(request_data, payment)
    else:
        return ('Invalid request body field.', HTTPStatus.BAD_REQUEST.value)
    

    # insert the object into the database
    if not payment.insert():
        return ('Server error.', HTTPStatus.INTERNAL_SERVER_ERROR.value)
    
    # return the url to the newly created resource
    return flask.jsonify(payment.get())

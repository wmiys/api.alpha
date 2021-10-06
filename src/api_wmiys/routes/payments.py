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
@security.login_required
def getLocations():

    payment = Payment()
    payment.id = utilities.getUUID(True)
    payment.renter_id = security.requestGlobals.client_id

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
    # paymentApiUrl = f'''/payments/{payment.id}'''
    # return paymentApiUrl
    return str(payment.id)

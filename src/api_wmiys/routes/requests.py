"""
Package:        requests
Url Prefix:     /requests
Description:    Handles all the pproduct requests.
"""
import flask
from http import HTTPStatus
from flask import Blueprint
from ..common import security, utilities
from ..models import ProductRequest, product_request

# route blueprint
bp_requests = Blueprint('bp_requests', __name__)

#-----------------------------------------------------
# Create a new product request
# ----------------------------------------------------
@bp_requests.route('/submitted', methods=['POST'])
@security.login_required
def post():
    # transform the request form into a dict
    requestForm = flask.request.form.to_dict()

    # create the initial product request object
    productRequest = ProductRequest(renter_id=security.requestGlobals.client_id)

    # set the product request object's property values to the ones given in the request
    if utilities.areAllKeysValidProperties(requestForm, productRequest):  
        utilities.setPropertyValuesFromDict(requestForm, productRequest)
    else:
        return ('Request body contained an invalid field.', 400)

    # ensure the request had all the required fields
    if not productRequest.allPropertiesForInsertSet():
        return ('Missing a required request field.', 400)

    # insert the request into the database
    if productRequest.insert():
        return ('', HTTPStatus.CREATED)
    else:
        return ('Insert error', 400)

    

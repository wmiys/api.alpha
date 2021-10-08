"""
Package:        requests
Url Prefix:     /requests
Description:    Handles all the pproduct requests.
"""
import flask
from http import HTTPStatus
from ..common import security, utilities
from ..models import ProductRequest, product_request

# route blueprint
bp_requests = flask.Blueprint('bp_requests', __name__)

#-----------------------------------------------------
# Create a new product request for the lender.
# 
# This get's called from the front-end ONLY!!
# Normal users ARE NOT allowed to do this themselves.
# ----------------------------------------------------
@bp_requests.route('/received', methods=['POST'])
@security.login_required
def newRequest():
    productRequest = ProductRequest()

    requestData: dict = flask.request.form.to_dict()

    # set the object's attribute values from the incoming request form body
    if utilities.areAllKeysValidProperties(requestData, productRequest):
        utilities.setPropertyValuesFromDict(requestData, productRequest)
    else:
        return ('Invalid request body field.', HTTPStatus.UNPROCESSABLE_ENTITY.value)
    
    # make sure all the required object attributes are set in order to save the object 
    if not productRequest.areInsertAttributesSet():
        return ('Request body is missing a required field.', HTTPStatus.UNPROCESSABLE_ENTITY.value)

    # insert the object into the database
    if not productRequest.insert():
        return ('Error inserting the product request. Check log', HTTPStatus.INTERNAL_SERVER_ERROR.value)
    

    return ('', HTTPStatus.CREATED.value)


#-----------------------------------------------------
# Create a new product request for the lender.
# This get's called from the front-end ONLY!!
# Normal users ARE NOT allowed to do this themselves.
# ----------------------------------------------------
@bp_requests.route('/received', methods=['GET'])
@security.login_required
def getLenderRequests():
    
    return flask.jsonify(product_request.getReceived(security.requestGlobals.client_id))
    return 'received product requests'


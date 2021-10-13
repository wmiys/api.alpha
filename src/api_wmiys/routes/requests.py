"""
Package:        requests
Url Prefix:     /requests
Description:    Handles all the pproduct requests.
"""
import re
import flask
from http import HTTPStatus
from ..common import security, utilities
from ..models import ProductRequest, product_request

# route blueprint
bp_requests = flask.Blueprint('bp_requests', __name__)


LENDER_RESPONSE_ACCEPT = 'accept'
LENDER_RESPONSE_DECLINE = 'decline'


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
    requests = product_request.getReceived(security.requestGlobals.client_id)

    return flask.jsonify(requests)


#-----------------------------------------------------
# Retrieve a single received request
# ----------------------------------------------------
@bp_requests.route('/received/<int:request_id>', methods=['GET'])
@security.login_required
def getSingleRequest(request_id: int):
    request = ProductRequest(id=request_id)
    return flask.jsonify(request.getLender())


#-----------------------------------------------------
# Lender responds to a request with either accept or decline
# ----------------------------------------------------
@bp_requests.route('/received/<int:request_id>/<string:status>', methods=['POST'])
@security.login_required
def respondToRequest(request_id: int, status: str):
    # response url should be either accept or decline
    if status not in [LENDER_RESPONSE_ACCEPT, LENDER_RESPONSE_DECLINE]:
        return ("Status needs to be either 'accept' or 'decline'.", HTTPStatus.BAD_REQUEST.value)

    request = ProductRequest(id=request_id)
    
    if not request.load():
        return ('Could not find the request', HTTPStatus.NOT_FOUND.value)

    # make sure the client has not already responded to this request
    if request.status != product_request.RequestStatus.pending:
        return ('Already responded to this request', HTTPStatus.BAD_REQUEST.value)

    # set the new status in the object
    if status == LENDER_RESPONSE_ACCEPT:
        request.status = product_request.RequestStatus.accepted
    else:
        request.status = product_request.RequestStatus.denied

    # update the database record
    # only 1 record should be updated
    if request.updateStatus() == 1:
        return ('', HTTPStatus.NO_CONTENT.value)
    else:
        return ('Error updating the product request.', HTTPStatus.INTERNAL_SERVER_ERROR.value)


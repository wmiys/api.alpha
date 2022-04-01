"""
Package:        requests
Url Prefix:     /requests/received
Description:    Handles all the pproduct requests.
"""
import flask
from http import HTTPStatus
from uuid import UUID
from wmiys_common import utilities
from ..common import security
from ..models import ProductRequest, RequestStatus, product_request
from .. import payments


from api_wmiys.services import requests_received as requests_received_services


# route blueprint
bp_requests_received = flask.Blueprint('bp_requests_received', __name__)

LENDER_RESPONSE_ACCEPT = 'accept'
LENDER_RESPONSE_DECLINE = 'decline'

# global variable to hold the information of a lender product request response
m_product_request: ProductRequest = None


#-----------------------------------------------------
# Create a new product request for the lender.
# 
# This get's called from the front-end ONLY!!
# Normal users are NOT allowed to do this themselves.
# ----------------------------------------------------
@bp_requests_received.post('')
@security.no_external_requests
@security.login_required
def newRequest():
    product_request = ProductRequest(
        id = utilities.getUUID(False)
    )

    incoming_data: dict = flask.request.form.to_dict()

    # set the object's attribute values from the incoming request form body
    if utilities.areAllKeysValidProperties(incoming_data, product_request):
        utilities.setPropertyValuesFromDict(incoming_data, product_request)
    else:
        return ('Invalid request body field.', HTTPStatus.UNPROCESSABLE_ENTITY.value)

    
    # make sure all the required object attributes are set in order to save the object 
    if not product_request.areInsertAttributesSet():
        return ('Request body is missing a required field.', HTTPStatus.UNPROCESSABLE_ENTITY.value)

    # insert the object into the database
    if not product_request.insert():
        return ('Error inserting the product request. Check log', HTTPStatus.INTERNAL_SERVER_ERROR.value)
    

    return ('', HTTPStatus.CREATED.value)


#-----------------------------------------------------
# Get all received product requests
# ----------------------------------------------------
@bp_requests_received.get('')
@security.login_required
def getLenderRequests():
    return requests_received_services.responses_GET_ALL()


#-----------------------------------------------------
# Retrieve a single received request
# ----------------------------------------------------
@bp_requests_received.get('<uuid:request_id>')
@security.login_required
def getSingleRequest(request_id: UUID):
    return requests_received_services.responses_GET(request_id)


#-----------------------------------------------------
# Lender responds to a request with either accept or decline
# ----------------------------------------------------
@bp_requests_received.post('<uuid:request_id>/<string:status>')
@security.login_required
def respondToRequest(request_id: UUID, status: str):
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
        request.status = RequestStatus.accepted
    else:
        request.status = RequestStatus.denied

    global m_product_request
    m_product_request = request

    # update the database record
    # only 1 record should be updated
    if request.updateStatus() == 1:
        return ('', HTTPStatus.NO_CONTENT.value)
    else:
        return ('Error updating the product request.', HTTPStatus.INTERNAL_SERVER_ERROR.value)


#-----------------------------------------------------
# Code to run after the request.
#
# This code is responsible for capturing the payment funds
# from the lender once the lender accepts a pending product request.
# ----------------------------------------------------
@bp_requests_received.after_request
def afterLenderResponse(response: flask.Response):
    global m_product_request

    # ignore this code if the request wasn't a lender responding to a request
    if not m_product_request:
        return response
    
    if m_product_request.status == RequestStatus.accepted:
        payments.capturePayment(m_product_request.session_id)
    else:
        payments.cancelPayment(m_product_request.session_id)

    # reset the global variable to none so we don't double charge them
    m_product_request = None

    return response


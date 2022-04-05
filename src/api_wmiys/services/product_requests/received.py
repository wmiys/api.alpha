"""
**********************************************************************************************
Product requests are what the name implies... a renter has found a listing that is available
during the given start/end range, the renter has successfully paid for the product rental with stripe
and we have collected the funds. Now, the lender needs to finally approve the product rental with 
the renter.

Initially, a request status is set to 'pending'. The lender has 24 hours to respond to the 
request before being marked as 'expired' and the renter is fully refunded (and the request
cannot be responded to). Lenders can respond to a requests by either accepting or denying them.

Once a request status is either responded to or it expires, lenders cannot update a request.
**********************************************************************************************
"""

from __future__ import annotations
from datetime import datetime
from uuid import UUID
from enum import Enum, auto

import flask

from wmiys_common import utilities
from api_wmiys import payments
from api_wmiys.domain import models
from api_wmiys.domain.enums.product_requests import RequestStatus, LenderRequestResponse
from api_wmiys.common import responses, serializers
from api_wmiys.common.base_return import BaseReturn
from api_wmiys.services.product_requests import requests as requests_services
from api_wmiys.repository.product_requests import received as requests_received_repo


# Validation return codes for validating a request response from the lender
class RequestResponseValidation(Enum):
    VALID              = auto()
    NOT_FOUND          = auto()
    UNAUTHORIZED       = auto()
    ALREADY_RESPONDED  = auto()
    INVALID_STATUS_URL = auto()


#-----------------------------------------------------
# Create a new product request for the lender.
# ----------------------------------------------------
def responses_POST() -> flask.Response:
    pr = _generateNewModelFromRequest()

    if not _validateNewRequestAttributes(pr):
        return responses.badRequest('Missing a required key')

    
    db_result = requests_services.insert(pr)

    if not db_result.successful:
        return responses.badRequest(str(db_result.error))

    output = _getView(pr.id)

    return responses.created(output)


# Create a new product request model from the request's form data and assign it a new id
def _generateNewModelFromRequest() -> models.ProductRequest:
    # extract the form data
    form = flask.request.form.to_dict()
    serializer = serializers.ProductRequestSerializer(form)
    pr = serializer.serialize().model

    # generate a new UUID for the product request
    pr.id = utilities.getUUID(False)
    pr.created_on = datetime.now()  

    return pr


# Make sure the given product request's required attributes (for insertion) have values
def _validateNewRequestAttributes(pr: models.ProductRequest) -> bool:
    required_attributes = [
        pr.id,
        pr.payment_id,
        pr.session_id,
    ]

    if None in required_attributes:
        return False
    else:
        return True


#-----------------------------------------------------
# Get all received product requests
# ----------------------------------------------------
def responses_GET_ALL() -> flask.Response:
    request_status = _getStatusFromUrl()
    requests = []

    try:
        if not request_status:
            requests = _getAllViews(flask.g.client_id)
        else:
            requests = _getAllViewsByStatus(flask.g.client_id, request_status)
    
    except Exception as ex:
        return responses.badRequest(str(ex))

    return responses.get(requests)


#-----------------------------------------------------
# If the client provided a status url parm value, return it if it's valid, otherwise return null
#-----------------------------------------------------
def _getStatusFromUrl() -> RequestStatus | None:
    status_arg = flask.request.args.get('status')

    try:
        request_status = RequestStatus(status_arg.lower())
    except Exception:
        request_status = None   # client provided an invalid status value, so return null

    return request_status
    

#-----------------------------------------------------
# Get all the received product requests for the given user id
#-----------------------------------------------------
def _getAllViews(user_id) -> list[dict]:
    result = requests_received_repo.selectAll(user_id)

    if not result.successful:
        raise result.error
    
    views = result.data or []

    return views

#-----------------------------------------------------
# Get all the received product requests with the given status for the given user id
#-----------------------------------------------------
def _getAllViewsByStatus(user_id, status: RequestStatus) -> list[dict]:
    result = requests_received_repo.selectAllByStatus(user_id, status)

    if not result.successful:
        raise result.error
    
    views = result.data or []

    return views

#-----------------------------------------------------
# Retrieve a single received request
# ----------------------------------------------------
def responses_GET(request_id: UUID) -> flask.Response:

    try:
        request_view = _getView(request_id)
    except Exception as e:
        return responses.internal_error(str(e))
    
    if not request_view:
        return responses.notFound()
    
    return responses.get(request_view)


#-----------------------------------------------------
# Get the request view from the repository
#-----------------------------------------------------
def _getView(request_id) -> dict:
    result = requests_received_repo.select(request_id, flask.g.client_id)

    if not result.successful:
        raise result.error
    
    return result.data

#-----------------------------------------------------
# Lender responds to an existing product request
#-----------------------------------------------------
def responses_POST_STATUS(request_id: UUID, status: str) -> flask.Response:
    # get a product request model
    pr_internal = requests_services.getInternalModel(request_id)

    # validate it
    validation_result = _validateRequestResponse(pr_internal, status)

    if validation_result != RequestResponseValidation.VALID:
        return _invalidPost(validation_result)


    # turn the internal model into a ProductRequest domain model
    new_status = _getRequestStatusFromResponse(LenderRequestResponse(status))
    pr = _getBaselineModelResponsed(pr_internal, new_status)

    # process the payment
    payment_result = _processPayment(pr)

    # if not payment_result.successful:
        # return responses.badRequest(str(payment_result.error))

    # update the database
    update_db_result = requests_services.update(pr)

    if not update_db_result.successful:
        return responses.badRequest(str(update_db_result.error))

    # return the view
    view = requests_received_repo.select(pr.id, flask.g.client_id).data
    
    return responses.updated(view)


#-----------------------------------------------------
# Do some validation for request responses:
#   - check if request exists
#   - check if lender has authorization
#   - Check if it has already been responded to
#   - Check if the status is either 'accept' or 'decline'
#-----------------------------------------------------
def _validateRequestResponse(pr_internal: models.ProductRequestInternal, new_status: str) -> RequestResponseValidation:
    # make sure the request exists
    if not pr_internal:
        return RequestResponseValidation.NOT_FOUND

    # make sure the client's user_id matches the request's lender id
    if pr_internal.lender.id != flask.g.client_id:
        return RequestResponseValidation.UNAUTHORIZED

    # Check if it has already been responded to
    if pr_internal.status != RequestStatus.PENDING:
        return RequestResponseValidation.ALREADY_RESPONDED

    # Check if the status is either 'accept' or 'decline'
    try:
        LenderRequestResponse(new_status)
    except Exception as ex:
        return RequestResponseValidation.INVALID_STATUS_URL

    return RequestResponseValidation.VALID


#-----------------------------------------------------
# Handle an invalid post request
#-----------------------------------------------------
def _invalidPost(validation_error: RequestResponseValidation) -> flask.Response:
    if validation_error == RequestResponseValidation.NOT_FOUND:
        return responses.notFound()
    elif validation_error == RequestResponseValidation.UNAUTHORIZED:
        return responses.notFound()
    elif validation_error == RequestResponseValidation.ALREADY_RESPONDED:
        return responses.badRequest('Already responded to this request')
    elif validation_error == RequestResponseValidation.INVALID_STATUS_URL:
        return responses.badRequest("Status needs to be either 'accept' or 'decline'.")
    else:
        return responses.badRequest((validation_error.name, validation_error.value))

#-----------------------------------------------------
# turn the internal model into a ProductRequest domain model
#-----------------------------------------------------
def _getBaselineModelResponsed(internal_product_request: models.ProductRequestInternal, status: RequestStatus) -> models.ProductRequest:
    product_request = models.ProductRequest(
        id           = internal_product_request.id,
        payment_id   = internal_product_request.payment.id,
        session_id   = internal_product_request.session_id,
        status       = status,
        responded_on = datetime.now(),
        created_on   = internal_product_request.created_on
    )

    return product_request


def _getRequestStatusFromResponse(reply: LenderRequestResponse) -> RequestStatus:
    if LenderRequestResponse(reply) == LenderRequestResponse.ACCEPT:
        return RequestStatus.ACCEPTED
    else:
        return RequestStatus.DENIED


#-----------------------------------------------------
# Capture or cancel the given request's payment
#-----------------------------------------------------
def _processPayment(product_request: models.ProductRequest) -> BaseReturn:
    result = BaseReturn(successful=True)

    # determine which payment method to utilize
    if product_request.status == RequestStatus.ACCEPTED:
        payment_capture_method = payments.capturePayment
    else:
        payment_capture_method = payments.cancelPayment

    # try executing it
    try:
        result.data = payment_capture_method(product_request.session_id)
    except Exception as e:
        result.successful = False
        result.error = e

    return result


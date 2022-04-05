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
from urllib.request import Request
import flask
from api_wmiys.domain import models
from api_wmiys.domain.enums.product_requests import RequestStatus

from api_wmiys.repository.product_requests import submitted as product_requests_submitted_repo
from api_wmiys.common import responses


#-----------------------------------------------------
# Get all SUBMITTED requests
# ----------------------------------------------------
def responses_GET_ALL() -> flask.Response:
    status_filter = _getStatusUrlParm()

    if status_filter:
        requests = _getAllViewsByStatus(flask.g.client_id, status_filter)
    else:
        requests = _getAllViews(flask.g.client_id)
        
    return responses.get(requests)

# ----------------------------------------------------
# If a 'status' url query parm was given in the request, transform it into a RequestStatus object
# Otherwise, return null
# ----------------------------------------------------
def _getStatusUrlParm() -> RequestStatus | None:
    status_arg = flask.request.args.get('status') or None

    try:
        request_status = RequestStatus(status_arg)
    except ValueError:
        request_status = None
    
    return request_status


# Get all request views submitted by the given renter
def _getAllViews(renter_id) -> list[dict]:
    db_result = product_requests_submitted_repo.selectAll(renter_id)

    if not db_result.successful:
        raise db_result.error
    
    return db_result.data or []


#-----------------------------------------------------
# Retrieve all the requests that a renter has submitted
# that have the specified status.
# 
# Parms:
#   renter_id: the renter's user_id
#   status: the status to filter by
# ----------------------------------------------------
def _getAllViewsByStatus(renter_id, status: RequestStatus) -> list[dict]:
    db_result = product_requests_submitted_repo.selectAllByStatus(renter_id, status)

    if not db_result.successful:
        raise db_result.error
    
    return db_result.data or []

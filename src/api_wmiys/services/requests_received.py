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
import flask
from api_wmiys.domain import models
from api_wmiys.domain.enums.requests import RequestStatus
from api_wmiys.repository import requests_received as requests_received_repo
from api_wmiys.common import responses


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




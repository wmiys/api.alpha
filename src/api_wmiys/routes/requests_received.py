"""
**********************************************************************************************
Package:        requests
Url Prefix:     /requests/received
Description:    Handles all the pproduct requests.
**********************************************************************************************
"""

import flask
from uuid import UUID

from api_wmiys.common import security
from api_wmiys.services.product_requests import received as requests_received_services

# route blueprint
bp_requests_received = flask.Blueprint('bp_requests_received', __name__)


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
    return requests_received_services.responses_POST()

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
    return requests_received_services.responses_POST_STATUS(request_id, status)



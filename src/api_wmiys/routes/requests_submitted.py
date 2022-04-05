"""
**********************************************************************************************
Package:        requests
Url Prefix:     /requests/submitted
Description:    Handles all the submitted product requests (client is the renter).
**********************************************************************************************
"""

from uuid import UUID

import flask

from api_wmiys.common import security
from api_wmiys.services.product_requests import submitted as product_requests_submitted_services

# route blueprint
bp_requests_submitted = flask.Blueprint('bp_requests_submitted', __name__)

#-----------------------------------------------------
# Get all SUBMITTED requests
# ----------------------------------------------------
@bp_requests_submitted.get('')
@security.login_required
def getSubmittedAll():
    return product_requests_submitted_services.responses_GET_ALL()


#-----------------------------------------------------
# Get a single SUBMITTED request
# ----------------------------------------------------
@bp_requests_submitted.get('<uuid:request_id>')
@security.login_required
def getSubmitted(request_id: UUID):
    return product_requests_submitted_services.responses_GET(request_id)

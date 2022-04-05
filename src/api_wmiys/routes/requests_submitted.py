"""
Package:        requests
Url Prefix:     /requests/submitted
Description:    Handles all the pproduct requests.
"""
import flask
from http import HTTPStatus
from uuid import UUID
from ..common import security
from ..models import ProductRequest, RequestStatus, product_request

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

    status_arg = flask.request.args.get('status')

    try:
        # try to parse the status url query parm
        request_status = RequestStatus(status_arg)
        
        requests = product_request.getSubmittedFilterByStatus(
            renter_id = flask.g.client_id,
            status    = RequestStatus(request_status)
        )

    except ValueError:
        # client provided an invalid status value... so return all of them
        requests = product_request.getSubmitted(flask.g.client_id)

    return flask.jsonify(requests)


#-----------------------------------------------------
# Get a single SUBMITTED request
# ----------------------------------------------------
@bp_requests_submitted.get('<uuid:request_id>')
@security.login_required
def getSubmitted(request_id: UUID):
    request = ProductRequest(id=request_id)
    request_dict = request.getRenter()

    if request_dict.get('renter_id') != flask.g.client_id:
        return ('', HTTPStatus.FORBIDDEN.value)

    return flask.jsonify(request_dict)

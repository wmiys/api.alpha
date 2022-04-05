"""
**********************************************************************************************

Submitted product request services.

This is for retrieving all submitted product requests. Or, the client is the renter.

**********************************************************************************************
"""

from __future__ import annotations
from uuid import UUID

import flask

from api_wmiys.common import responses
from api_wmiys.domain.enums.product_requests import RequestStatus
from api_wmiys.repository.product_requests import submitted as product_requests_submitted_repo
from api_wmiys.services.product_requests import requests as product_request_services


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

#-----------------------------------------------------
# Get all request views submitted by the given renter
#-----------------------------------------------------
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


#-----------------------------------------------------
# Get a single SUBMITTED request
# ----------------------------------------------------
def responses_GET(product_request_id: UUID) -> flask.Response:
    # make sure the client is authorized to view the request
    try:
        if not _isClientAuthorized(product_request_id):
            return responses.notFound()
    except Exception as ex:
        return responses.badRequest(str(ex))
    
    # now get the view from the database
    try:
        request_view = _getView(product_request_id)
    except Exception as ex:
        return responses.badRequest(str(ex))

    return responses.get(request_view)


#-----------------------------------------------------
# make sure the request exists and the client is authorized to view it
#-----------------------------------------------------
def _isClientAuthorized(product_request_id) -> bool:
    # fetch an internal product request model
    pr_internal = product_request_services.getInternalModel(product_request_id)
    
    # make sure the request exists and the client is authorized to view it
    if not pr_internal:
        return False
    elif pr_internal.renter.id != flask.g.client_id:
        return False
    
    return True

#-----------------------------------------------------
# Get the database view of the specified product request
#-----------------------------------------------------
def _getView(product_request_id) -> dict | None:
    db_result = product_requests_submitted_repo.select(product_request_id)

    if not db_result.successful:
        raise db_result.error

    return db_result.data

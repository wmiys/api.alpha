"""
**********************************************************************************************

Submitted product request services.

This is for retrieving all submitted product requests. Or, the client is the renter.

**********************************************************************************************
"""

from __future__ import annotations
from enum import Enum
from uuid import UUID

import flask
from wmiys_common import utilities

from api_wmiys.common import responses
from api_wmiys.common import images
from api_wmiys.common import serializers
from api_wmiys.common import BaseReturn
from api_wmiys.domain import models
from api_wmiys.domain.enums.product_requests import RequestStatus
from api_wmiys.repository.product_requests import submitted as product_requests_submitted_repo
from api_wmiys.services.product_requests import requests as product_request_services


class UpdateValidationResult(str, Enum): 
    VALID                    = 'valid'
    SCORE_NOT_INT            = 'review_score mut be a valid integer'
    SCORE_NOT_IN_RANGE       = 'review_score must be between 0-5'
    COMMENT_LENGTH_TOO_LARGE = 'review_comment cannot exceed 500 characters'

class UpdateValidationConstants:
    DEFAULT_SCORE_VALUE = 1
    SCORE_RANGE_MIN     = 0
    SCORE_RANGE_MAX     = 5
    COMMENT_MAX_LENGTH  = 500


#-----------------------------------------------------
# Get all SUBMITTED requests
# ----------------------------------------------------
def responses_GET_ALL() -> flask.Response:
    status_filter = _getStatusUrlParm()

    if status_filter:
        requests = _getAllViewsByStatus(flask.g.client_id, status_filter)
    else:
        requests = _getAllViews(flask.g.client_id)

    requests_prefixed = _prefixImageValuesUrl(requests)

    return responses.get(requests_prefixed)

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
# prefix the product image value with the server static url
#-----------------------------------------------------
def _prefixImageValuesUrl(requests: list[dict]) -> list[dict]:
    # prefix the image values with the url
    url_prefix = images.getCoverUrl()

    for request in requests:
        original_image_value = request.get('product_image') or None

        if not original_image_value:
            continue

        request['product_image'] = f'{url_prefix}{original_image_value}'

    return requests


#-----------------------------------------------------
# Update a single SUBMITTED request
# ----------------------------------------------------
def responses_PATCH(product_request_id: UUID) -> flask.Response:
    if not _isClientAuthorized(product_request_id):
        return responses.notFound()
    
    model = _getExistingModel(product_request_id)

    if not model:
        return responses.notFound()
    
    form = flask.request.form.to_dict()

    # get the review request body values (if they were provided)
    model.review_score = form.get('review_score') or model.review_score
    model.review_comment = form.get('review_comment') or model.review_comment

    # validate it
    validation = _validateUpdatedModel(model)

    if validation != UpdateValidationResult.VALID:
        return responses.badRequest(validation)

    try:
        _updateModel(model)
        updated_view = _getView(product_request_id)
        
        return responses.updated(updated_view)
    
    except Exception as ex:
        return responses.badRequest(str(ex))


#-----------------------------------------------------
# Get the existing domain model
#-----------------------------------------------------
def _getExistingModel(product_request_id: UUID) -> models.ProductRequest | None:
    view = _getView(product_request_id)

    if view:
        return _seriaizeDict(view)
    else:
        return None

#-----------------------------------------------------
# Get the database view of the specified product request
#-----------------------------------------------------
def _getView(product_request_id) -> dict | None:
    db_result = product_requests_submitted_repo.select(product_request_id)

    if not db_result.successful:
        raise db_result.error

    return db_result.data or None

#-----------------------------------------------------
# Serialize the given dictionary into a ProductRequest model
#-----------------------------------------------------
def _seriaizeDict(model_dict: dict) -> models.ProductRequest:
    serializer = serializers.ProductRequestSerializer(model_dict)
    model = serializer.serialize().model

    return model

#-----------------------------------------------------
# Update the specified request model in the database
#-----------------------------------------------------
def _updateModel(product_request: models.ProductRequest):
    db_result = product_requests_submitted_repo.update(product_request)

    if not db_result.successful:
        raise db_result.error

#-----------------------------------------------------
# Run some validation checks on the given request model
#-----------------------------------------------------
def _validateUpdatedModel(product_request: models.ProductRequest) -> UpdateValidationResult:

    try:
        score = int(product_request.review_score) or UpdateValidationConstants.DEFAULT_SCORE_VALUE
    except (ValueError, TypeError) as error:
        return UpdateValidationResult.SCORE_NOT_INT

    if not utilities.inRange(score, UpdateValidationConstants.SCORE_RANGE_MIN, UpdateValidationConstants.SCORE_RANGE_MAX):
        return UpdateValidationResult.SCORE_NOT_IN_RANGE

    try:
        comment_length = len(product_request.review_comment)
    except:
        comment_length = 1

    if comment_length > UpdateValidationConstants.COMMENT_MAX_LENGTH:
        return UpdateValidationResult.COMMENT_LENGTH_TOO_LARGE

    return UpdateValidationResult.VALID


    
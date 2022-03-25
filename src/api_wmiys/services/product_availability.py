"""
**********************************************************************************************
A product availability record represents a lender provided date range that they do not wish for
their product to be available for rent. 

So renters will not be able to see the product in the search results if their start/end date range
conflicts with any product availability record.

Furthermore, products that have conflicting availability records will not be able to even receive 
requests from renters if the starts/ends range conflicts.
**********************************************************************************************
"""
from __future__ import annotations
from collections import namedtuple
import datetime
import flask
from wmiys_common import utilities
from api_wmiys.repository import product_availability as product_availability_repo
from api_wmiys.common import responses
from api_wmiys.common import serializers
from api_wmiys.domain import models


#----------------------------------------------------------
# Parm block for _standardModifyResponse
#
# Parms:
#     product_availability_id:  the product availability's id (either provided in the request URL or a new one is generated)
#     product_id:               the parent product's id
#     repository_callback:      api_wmiys.repository.product_availability callback function
#     responses_callback:       api_wmiys.common.responses callback function
#----------------------------------------------------------
ModifyRequestParms = namedtuple("ModifyRequestParms", "product_availability_id product_id repository_callback responses_callback")


#----------------------------------------------------------
# Respond to a GET ALL request
#----------------------------------------------------------
def responses_GET_ALL(product_id) -> flask.Response:
    result = product_availability_repo.selectAll(product_id)

    if not result.successful:
        return responses.badRequest(str(result.error))

    return responses.get(result.data)


#----------------------------------------------------------
# Respond to a POST request
#----------------------------------------------------------
def responses_POST(product_id) -> flask.Response:
    parms = ModifyRequestParms(
        product_availability_id = utilities.getUUID(False),             # generate a new UUID
        product_id              = product_id,
        repository_callback     = product_availability_repo.insert,
        responses_callback      = responses.created
    )

    return _standardModifyResponse(parms)

#----------------------------------------------------------
# Respond to a PUT request
#----------------------------------------------------------
def responses_PUT(product_id, product_availability_id) -> flask.Response:    
    parms = ModifyRequestParms(
        product_availability_id = product_availability_id,
        product_id              = product_id,
        repository_callback     = product_availability_repo.update,
        responses_callback      = responses.updated
    )

    return _standardModifyResponse(parms)

#----------------------------------------------------------
# Standardized response routine for POST or PUT requests
#----------------------------------------------------------
def _standardModifyResponse(modify_parms: ModifyRequestParms) -> flask.Response:
    # extract the request's form data into a ProductAvailability model
    product_availability = _extractFormData()

    # make sure the model is correct and has correct values
    if not _isModelValid(product_availability):
        return responses.badRequest('Invalid form data.')

    # explicitly set the model's new id and it's parent product id
    product_availability.id         = modify_parms.product_availability_id
    product_availability.product_id = modify_parms.product_id

    # insert the record into the database
    result = modify_parms.repository_callback(product_availability)

    if not result.successful:
        return responses.badRequest(str(result.error))

    return _standardViewReturn(modify_parms.product_availability_id, modify_parms.responses_callback)

#----------------------------------------------------------
# Extract the request's form data into a ProductAvailability model
#----------------------------------------------------------
def _extractFormData() -> models.ProductAvailability:
    form         = flask.request.form.to_dict()
    serializer   = serializers.ProductAvailabilitySerializer(form)
    availability = serializer.serialize().model

    return availability

#----------------------------------------------------------
# Validates the given ProductAvailability is okay to save in the database:
#
#   - Both starts_on and ends_on need to have values (not null)
#   - Both starts_on and ends_on need to be a valid date
#   - ends_on needs to be at least 1 day AFTER starts_on
#   - starts_on needs cannot be anything less than today's date
#
# Returns false if any of those conditions are false, otherwise true.
#----------------------------------------------------------
def _isModelValid(product_availability: models.ProductAvailability) -> bool:

    today = datetime.datetime.now().date()

    if None in [product_availability.starts_on, product_availability.ends_on]:
        return False
    elif not isinstance(product_availability.starts_on, datetime.date):
        return False
    elif not isinstance(product_availability.ends_on, datetime.date):
        return False
    elif product_availability.ends_on <= product_availability.starts_on:
        return False
    elif product_availability.starts_on < today:
        return False
    else:
        return True


#----------------------------------------------------------
# Respond to a GET request
#----------------------------------------------------------
def responses_GET(product_availability_id) -> flask.Response:
    return _standardViewReturn(product_availability_id, responses.get)


#----------------------------------------------------------
# Standardized way to fetch the ProductAvailability view response
#----------------------------------------------------------
def _standardViewReturn(product_availability_id, responses_callback) -> flask.Response:
    result = product_availability_repo.select(product_availability_id)

    if not result.successful:
        return responses.badRequest(str(result.error))
    elif not result.data:
        return responses.notFound()

    return responses_callback(result.data)


#----------------------------------------------------------
# Respond to a DELETE request
#----------------------------------------------------------
def responses_DELETE() -> flask.Response:
    pass






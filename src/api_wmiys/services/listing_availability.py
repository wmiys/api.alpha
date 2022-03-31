"""
**********************************************************************************************

A product listing availability has 1 responsibility: checking if the product is available to rent given the parms.

**********************************************************************************************
"""

import flask
from api_wmiys.domain import models
from api_wmiys.domain.enums.sql import SqlBool
from api_wmiys.common import serializers
from api_wmiys.common import responses
from api_wmiys.common import DateRangeValidator
from api_wmiys.common import ValidationReturnCodes
from api_wmiys.common.base_return import BaseReturn
from api_wmiys.repository import listing_availability as listing_availability_repo

#----------------------------------------------------------
# Check if a product is available for rent
#----------------------------------------------------------
def responses_GET(product_id) -> flask.Response:
    # serialize the request url arguments into a ProductListingAvailability domain model
    model = _serializeRequestUrlParms()
    model.product_id = product_id

    # perform some validation
    validation_result = _validateModel(model)

    if not validation_result.successful:
        return responses.badRequest(str(validation_result.error))

    # run the model through the mysql algorithm to see if it is available
    is_available = _isProductAvailable(model)

    return responses.get(dict(available=is_available))

#----------------------------------------------------------
# Serialize the request form data into a domain model
#----------------------------------------------------------
def _serializeRequestUrlParms() -> models.ProductListingAvailability:
    form       = flask.request.args.to_dict()
    serializer = serializers.ProductListingAvailabilitySerializer(form)
    result     = serializer.serialize()

    return result.model

#----------------------------------------------------------
# Validate the given model
#----------------------------------------------------------
def _validateModel(listing_availability: models.ProductListingAvailability) -> BaseReturn:
    # assume the range is not valid
    result = BaseReturn(successful=False)

    # make sure all the required attributes are set
    if _missingAttributeValues(listing_availability):
        result.error = 'Missing one or more required url paramters'
        return result
    
    # validate the date range
    dates_validation_result = _validateModelDates(listing_availability)

    if not dates_validation_result.successful:
        result.error = dates_validation_result.error
        return result
    
    result.successful = True
    
    return result

#----------------------------------------------------------
# Checks if any of the model's required attribute values are null
# Returns true if one of them are null, otherwise false (good to go)
#----------------------------------------------------------
def _missingAttributeValues(listing_availability: models.ProductListingAvailability) -> bool:
    required_attributes = [
        listing_availability.product_id,
        listing_availability.location_id,
        listing_availability.starts_on,
        listing_availability.ends_on,
    ]

    if None in required_attributes:
        return True
    else:
        return False


#----------------------------------------------------------
# Validate the model's starts_on/ends_on values
#----------------------------------------------------------
def _validateModelDates(listing_availability: models.ProductListingAvailability) -> BaseReturn:
        # assume the range is valid
    result = BaseReturn(successful=True)

    range_validator = DateRangeValidator(
        start = listing_availability.starts_on,
        end = listing_availability.ends_on,
    )

    range_validator_result = range_validator.validate()

    if not range_validator_result == ValidationReturnCodes.VALID:
        result.error = range_validator_result.name
        result.successful = False
    
    return result

#----------------------------------------------------------
# Check if a product is available for rent
#----------------------------------------------------------
def _isProductAvailable(model: models.ProductListingAvailability) -> bool:
    db_result = listing_availability_repo.select(model)

    if not db_result.successful:
        raise db_result.error

    record_set: dict = db_result.data or dict()

    if not 'result' in record_set.keys():
        return False

    sql_bool = record_set.get('result') or SqlBool.FALSE

    try:
        result = SqlBool(sql_bool)
    except Exception as e:
        print(e)
        result = SqlBool.FALSE

    return result == SqlBool.TRUE







"""
**********************************************************************************************
This class represents a payment record in the database.

payment_session_id represents the session_id generated from the stripe API.

A payment occurs when a renter finds a product that they want to rent, and they have successfully
gave stripe their card information and it was successfully charged.
**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from datetime import datetime
from enum import Enum

import flask

from wmiys_common import utilities

from api_wmiys.domain import models
from api_wmiys.domain.enums.payments import DefaultFees
from api_wmiys.common import serializers
from api_wmiys.common import responses
from api_wmiys.common import base_return


# Possible validation errors
class ValidationErrors(str, Enum):
    MISSING_REQUIRED_FIELDS     = 'MISSING_REQUIRED_FIELDS'
    INVALID_DATE_STR_STARTS_ON  = 'INVALID_DATE_STR_STARTS_ON'
    INVALID_DATE_STR_ENDS_ON    = 'INVALID_DATE_STR_ENDS_ON'
    ENDS_ON_LESS_THAN_STARTS_ON = 'ENDS_ON_LESS_THAN_STARTS_ON'
    STARTS_ON_LESS_THAN_TODAY   = 'STARTS_ON_LESS_THAN_TODAY'


# Return value for request data validation
@dataclass
class ValidationReturn(base_return.BaseReturn):
    data: ValidationErrors = None


#------------------------------------------------------
# Create a new payment record
#------------------------------------------------------
def responses_POST() -> flask.Response:

    # serialize the incoming request data into a Payment domain model for validation
    payment_model = _getNewModelFromForm()

    # validate the request data model
    validation_result = _validateModel(payment_model)

    if not validation_result.successful:
        return responses.badRequest(validation_result.data.value)



    return responses.created(payment_model)


# Create a new Payment model from the form data and 
# generate a new UUID for the ID field
# set the renter_id attribute to the request's client id
def _getNewModelFromForm() -> models.Payment:
    payment = _serializeFormData()

    # explicitly set some of the model's attribute values
    payment.id         = utilities.getUUID(False)
    payment.renter_id  = flask.g.client_id
    payment.created_on = datetime.now()
    payment.fee_lender = DefaultFees.LENDER.value
    payment.fee_renter = DefaultFees.RENTER.value


    return payment


# serialize the incoming request data into a Payment domain model for validation
def _serializeFormData() -> models.Payment:
    form          = flask.request.form.to_dict()
    serializer    = serializers.PaymentSerializer(form)
    payment_model = serializer.serialize().model

    return payment_model


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
def _validateModel(payment: models.Payment) -> ValidationReturn:
    result = ValidationReturn(successful=True)

    if not _areRequiredAttributesSet(payment):
        result.data = ValidationErrors.MISSING_REQUIRED_FIELDS
    elif not isinstance(payment.starts_on, date):
        result.data = ValidationErrors.INVALID_DATE_STR_STARTS_ON
    elif not isinstance(payment.ends_on, date):
        result.data = ValidationErrors.INVALID_DATE_STR_ENDS_ON
    elif payment.ends_on < payment.starts_on:
        result.data = ValidationErrors.ENDS_ON_LESS_THAN_STARTS_ON
    elif payment.starts_on < datetime.now().date():
        result.data = ValidationErrors.STARTS_ON_LESS_THAN_TODAY
    
    # if there was a validation error value, than means the model is invalid
    if result.data:
        result.successful = False

    return result

        
    



# Checks if all the required attributes have a value
def _areRequiredAttributesSet(payment: models.Payment) -> bool:
    required_fields = [
        payment.id,                    
        payment.product_id,    
        payment.renter_id, 
        payment.dropoff_location_id,   
        payment.starts_on,     
        payment.ends_on, 
        # payment.price_full,            
        payment.fee_lender,    
        payment.fee_renter,
    ]

    if None in required_fields:
        return False
    
    return True



"""
**********************************************************************************************

This module contains all the serializers.
A serializer transforms a dictionary into a domain model.

**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
import datetime
from uuid import UUID

import typing

from api_wmiys.domain import models
from api_wmiys.domain.enums.product_requests import RequestStatus

#------------------------------------------------------
# Result of the serialize method
#------------------------------------------------------
@dataclass
class SerializationResult:
    successful : bool      = False
    model      : dataclass = None

#------------------------------------------------------
# Base serializer class
#------------------------------------------------------
class SerializerBase:
    
    DomainModel: dataclass = object

    #------------------------------------------------------
    # Constructor
    #
    # Args:
    #   - dictionary: a dict of the data to serialize into the Domain Model
    #   - domain_model: an instance of the class' DomainModel or None
    #------------------------------------------------------
    def __init__(self, dictionary: dict, domain_model = None):
        self.dictionary = dictionary
        
        # if the given domain_model is not null, set the object's domain_model field to it
        # otherwise, call the contructor of the class' DomainModel
        self.domain_model = domain_model or self.DomainModel()

    #------------------------------------------------------
    # Serialize the object's dictionary into the sub-class' domain model
    #------------------------------------------------------
    def serialize(self) -> SerializationResult:
        result = SerializationResult(
            successful = True,
            model      = self.domain_model,
        )

        # get a list of all the Model's attributes
        model_keys = list(result.model.__annotations__.keys())

        # model_annotations = list(result.model.__annotations__.items())

        model_annotations  = typing.get_type_hints(type(result.model))

        # if the dict's key is an attribute in the model, copy over the value
        for key, value in self.dictionary.items():
            
            if not key in model_keys:
                result.successful = False
                continue

            if not value:
                setattr(result.model, key, None)
                continue

            # try:
            #     model_type = model_annotations.get(key)
            #     typecast_value = value

            #     if isinstance(value, (datetime.date, datetime.datetime)):
            #         typecast_value = model_type.fromisoformat(value)
            #     else:
            #         typecast_value = model_type(value)
            # except Exception as ex:
            #     pass
            #     # print(ex)
            # finally:
            #     setattr(result.model, key, typecast_value or None)

            setattr(result.model, key, value or None)

        return result

    #------------------------------------------------------
    # Parse the given datetime string into a python datetime/date object
    #
    # Args:
    #   datetime_module: either the datetime.datetime module or the datetime.date module (both have the fromisoformat function)
    #   date_string: the date string to parse
    #------------------------------------------------------
    def _parseIsoDatetime(self, datetime_module, date_string: str=None) -> datetime.datetime | str | None:
        if not date_string:
            return date_string
        
        try:
            result = datetime_module.fromisoformat(date_string)
        except Exception as e:
            result = date_string
            print(e)
        
        return result


#------------------------------------------------------
# Product
#------------------------------------------------------
class ProductSerializer(SerializerBase):
    DomainModel = models.Product

#------------------------------------------------------
# Location
#------------------------------------------------------
class LocationSerializer(SerializerBase):
    DomainModel = models.Location

#------------------------------------------------------
# User
#------------------------------------------------------
class UserSerializer(SerializerBase):
    DomainModel = models.User

#------------------------------------------------------
# Password Reset
#------------------------------------------------------
class PasswordResetSerializer(SerializerBase):
    DomainModel = models.PasswordReset


#------------------------------------------------------
# Payout Account
#------------------------------------------------------
class PayoutAccountSerializer(SerializerBase):
    DomainModel = models.PayoutAccount

    # need to do some additional processing for this data class
    def serialize(self) -> SerializationResult:
        serialization_result = super().serialize()

        if self.dictionary.get('confirmed', False) in [True, "true", "True"]:
            serialization_result.model.confirmed = True
        else:
            serialization_result.model.confirmed = False

        return serialization_result


#------------------------------------------------------
# Product Availability
#------------------------------------------------------
class ProductAvailabilitySerializer(SerializerBase):
    DomainModel = models.ProductAvailability

    #------------------------------------------------------
    # Parse the object's starts_on/ends_on values into date objects
    #------------------------------------------------------
    def serialize(self) -> SerializationResult:
        serialization_result = super().serialize()

        # parse the model's start/end times into date objects
        new_model: models.ProductAvailability = serialization_result.model
        new_model.starts_on = self._parseIsoDatetime(datetime.date, new_model.starts_on)
        new_model.ends_on = self._parseIsoDatetime(datetime.date, new_model.ends_on)

        # new_model.id = UUID(new_model.id)

        serialization_result.model = new_model

        return serialization_result


#------------------------------------------------------
# Product Images
#------------------------------------------------------
class ProductImageSerializer(SerializerBase):
    DomainModel = models.ProductImage


#------------------------------------------------------
# Payments
#------------------------------------------------------
class PaymentSerializer(SerializerBase):
    DomainModel = models.Payment

    #------------------------------------------------------
    # Parse the object's starts_on/ends_on values into date objects
    #------------------------------------------------------
    def serialize(self) -> SerializationResult:
        serialization_result = super().serialize()

        # parse the model's start/end times into date objects
        new_model: models.Payment = serialization_result.model
        new_model.starts_on = self._parseIsoDatetime(datetime.date, new_model.starts_on)
        new_model.ends_on = self._parseIsoDatetime(datetime.date, new_model.ends_on)

        # parse the dropoff_location_id into an int
        new_model.dropoff_location_id = int(new_model.dropoff_location_id)

        serialization_result.model = new_model

        return serialization_result


#------------------------------------------------------
# Product Listing Availability
#------------------------------------------------------
class ProductListingAvailabilitySerializer(SerializerBase):
    DomainModel = models.ProductListingAvailability

    #------------------------------------------------------
    # Parse the object's starts_on/ends_on values into date objects
    #------------------------------------------------------
    def serialize(self) -> SerializationResult:
        serialization_result = super().serialize()

        new_model: models.ProductListingAvailability = serialization_result.model

        # parse the model's start/end times into date objects
        new_model.starts_on = self._parseIsoDatetime(datetime.date, new_model.starts_on)
        new_model.ends_on = self._parseIsoDatetime(datetime.date, new_model.ends_on)

        if new_model.location_id:
            new_model.location_id = int(new_model.location_id)

        serialization_result.model = new_model

        return serialization_result


#------------------------------------------------------
# Product Images
#------------------------------------------------------
class ProductRequestSerializer(SerializerBase):
    DomainModel = models.ProductRequest

    #------------------------------------------------------
    # Parse the object's id into a UUID and status into a RequestStatus enum
    #------------------------------------------------------
    def serialize(self) -> SerializationResult:
        serialization_result = super().serialize()

        new_model = serialization_result.model
        
        if new_model.id:
            new_model.id = UUID(new_model.id)
        
        if new_model.status:
            new_model.status = RequestStatus(new_model.status)

        serialization_result.model = new_model

        return serialization_result


#------------------------------------------------------
# Balance transfers
#------------------------------------------------------
class BalanceTransferSerializer(SerializerBase):
    DomainModel = models.BalanceTransfer
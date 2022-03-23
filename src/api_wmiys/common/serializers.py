"""
**********************************************************************************************

This module contains all the serializers.
A serializer transforms a dictionary into a domain model.

**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass

from api_wmiys.domain import models

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

        # if the dict's key is an attribute in the model, copy over the value
        for key, value in self.dictionary.items():
            if not key in model_keys:
                result.successful = False

            setattr(result.model, key, value or None)

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
# User
#------------------------------------------------------
class UserSerializer(SerializerBase):
    DomainModel = models.User
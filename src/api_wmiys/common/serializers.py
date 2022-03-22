"""

This module contains all the serializers.

A serializer transforms a dictionary into a domain model.

"""

from dataclasses import dataclass
import flask
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
    #------------------------------------------------------
    def __init__(self, dictionary: dict):
        self.dictionary = dictionary

    #------------------------------------------------------
    # Serialize the object's dictionary into the sub-class' domain model
    #------------------------------------------------------
    def serialize(self) -> SerializationResult:
        result = SerializationResult(
            successful = True,
            model      = self.DomainModel(),
        )

        # get a list of all the Model's attributes
        model_keys = list(result.model.__annotations__.keys())

        # if the dict's key is an attribute in the model, copy over the value
        for key, value in self.dictionary.items():
            if not key in model_keys:
                result.successful = False

            setattr(result.model, key, value)

        return result



class ProductSerializer(SerializerBase):
    DomainModel = models.Product


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
            successful = False,
            model      = self.DomainModel(),
        )

        model_keys = list(result.model.__annotations__.keys())

        for key, value in self.dictionary.items():
            if not key in model_keys:
                return result

            setattr(result.model, key, value)

        result.successful = True
        return result



class ProductSerializer(SerializerBase):
    DomainModel = models.Product


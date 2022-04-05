
"""
**********************************************************************************************

Product Request routines

**********************************************************************************************
"""

from __future__ import annotations
from uuid import UUID
from enum import Enum
from api_wmiys.domain import models
from api_wmiys.repository.product_requests import requests as requests_repo
from api_wmiys.common import serializers
from api_wmiys.common.base_return import BaseReturn


class DbColumnPrefix(str, Enum):
    RENTER          = 'renter_'
    LENDER          = 'lender_'
    PAYMENT         = 'payment_'
    PRODUCT_REQUEST = 'product_request_'

#------------------------------------------------------
# Get the internal ProductRequest model.
# Returns None if it does not exist
#------------------------------------------------------
def getInternal(product_request_id: UUID) -> models.ProductRequestInternal | None:
    db_result = requests_repo.select(product_request_id)

    if not db_result.successful:
        raise db_result.error
    if not db_result.data:
        return None

    pr_internal = models.ProductRequestInternal()

    # get a normal ProductRequest model
    product_request_model = _getModel(db_result.data, DbColumnPrefix.PRODUCT_REQUEST, serializers.ProductRequestSerializer)

    # move over its attribute values into the internal product request object
    pr_internal.__dict__.update(vars(product_request_model))

    # add all the data models
    pr_internal.renter  = _getModel(db_result.data, DbColumnPrefix.RENTER, serializers.UserSerializer)
    pr_internal.lender  = _getModel(db_result.data, DbColumnPrefix.LENDER, serializers.UserSerializer)
    pr_internal.payment = _getModel(db_result.data, DbColumnPrefix.PAYMENT, serializers.PaymentSerializer)

    return pr_internal

#------------------------------------------------------
# Serialzie the dictionary using the specified serializer
#------------------------------------------------------
def _getModel(data: dict, prefix: DbColumnPrefix, SerializerClass: serializers.SerializerBase):
    # get the subset of key/values that have the specified prefix
    namespace_dict = _getNamespace(data, prefix.value)

    # serialize the dictionary into a domain model
    serializer = SerializerClass(namespace_dict)
    result = serializer.serialize()

    return result.model


#-----------------------------------------------------
# Returns a dictionary containing a subset of key/values that match the specified namespace/prefix. 
#
# Args:
#   namespace: a configuration namespace    
#   lowercase: a flag indicating if the keys of the resulting dictionary should be lowercase
#   trim: a flag indicating if the keys of the resulting dictionary should not include the namespace
#
# Copied from flask:
#   https://flask.palletsprojects.com/en/2.1.x/api/#flask.Config.get_namespace
#   https://github.com/pallets/flask/blob/f70abe634a7a058ce35b11893002a97085515b6f/src/flask/config.py#L293
#-----------------------------------------------------
def _getNamespace(data: dict, namespace: str, lowercase: bool=True, trim: bool=True) -> dict:
    return_value = {}
    
    for key, value in data.items():
        if not key.startswith(namespace):
            continue

        if trim:
            key = key[len(namespace) :]
        else:
            key = key

        if lowercase:
            key = key.lower()

        return_value[key] = value
    
    return return_value



def update(product_request: models.ProductRequest) -> BaseReturn:
    return _modify(product_request)



def _modify(product_request: models.ProductRequest) -> BaseReturn:
    db_result = requests_repo.update(product_request)

    result = BaseReturn()
    result.__dict__.update(vars(db_result))

    return result




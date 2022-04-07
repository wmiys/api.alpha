"""
**********************************************************************************************

This class is responsible for serializing the list of client data dictionaries into a Client domain model.

**********************************************************************************************
"""

from __future__ import annotations
from typing import Dict
from uuid import UUID

from api_wmiys.common import serializers
from api_wmiys.domain import models
from api_wmiys.domain.internal.client import Client, ClientRecordSetCollection

# Type alias
DictInt  = Dict[int, models.Product]
DictUuid = Dict[UUID, object]


class ClientRecordSetSerializer:

    #------------------------------------------------------ 
    # Constructor
    #------------------------------------------------------
    def __init__(self, records_collection: ClientRecordSetCollection):
        self.records_collection = records_collection


    #------------------------------------------------------ 
    # Serialize all the dictionary lists
    #------------------------------------------------------
    def serialize(self) -> Client:
        client = Client(
            products                   = self._serializeProduct(),
            product_availability       = self._serializeProductAvailability(),
            product_images             = self._serializeProductImages(),
            product_requests_received  = self._serializeProductRequestsReceived(),
            product_requests_submitted = self._serializeProductRequestsSubmitted(),
            payout_accounts            = self._serializePayoutAccounts(),
            balance_transfers          = self._serializeBalanceTransfers(),
        )
    
    
        return client

    def _serializeProduct(self) -> dict[int, models.Product]:
        return self._serializeBase(self.records_collection.products, serializers.ProductSerializer)
    
    def _serializeProductAvailability(self) -> DictUuid:
        return self._serializeBase(self.records_collection.product_availability, serializers.ProductAvailabilitySerializer)

    def _serializeProductImages(self) -> DictUuid:
        return self._serializeBase(self.records_collection.product_images, serializers.ProductImageSerializer)

    def _serializeProductRequestsReceived(self) -> DictUuid:
        return self._serializeBase(self.records_collection.product_requests_received, serializers.ProductRequestSerializer)

    def _serializeProductRequestsSubmitted(self) -> DictUuid:
        return self._serializeBase(self.records_collection.product_requests_submitted, serializers.ProductRequestSerializer)

    def _serializePayoutAccounts(self) -> DictUuid:
        return self._serializeBase(self.records_collection.payout_accounts, serializers.PayoutAccountSerializer)

    def _serializeBalanceTransfers(self) -> DictUuid:
        return self._serializeBase(self.records_collection.balance_transfers, serializers.BalanceTransferSerializer)

    def _serializeBase(self, dictionary_list: list[dict], serializer_class_type) -> dict:
        output = {}

        for dictionary in dictionary_list:
            serializer = serializer_class_type(dictionary)
            model = serializer.serialize().model

            if isinstance(model.id, UUID):
                output[str(model.id)] = model    
            else:
                output[model.id] = model

        return output


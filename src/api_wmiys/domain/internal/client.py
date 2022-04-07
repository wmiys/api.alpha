



from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID
from api_wmiys.domain import models


class RecordSetIndex:
    PRODUCTS                   = 0
    PRODUCT_AVAILABILITY       = 1
    PRODUCT_IMAGES             = 2
    PRODUCT_REQUESTS_RECEIVED  = 3
    PRODUCT_REQUESTS_SUBMITTED = 4
    BALANCE_TRANSFERS          = 5
    PAYOUT_ACCOUNTS            = 6


@dataclass
class ClientRecordSetCollection:
    products                   : list[dict] = None
    product_availability       : list[dict] = None
    product_images             : list[dict] = None
    product_requests_received  : list[dict] = None
    product_requests_submitted : list[dict] = None
    balance_transfers          : list[dict] = None
    payout_accounts            : list[dict] = None


@dataclass
class Client:
    products                   : dict[int, models.Product]              = None
    product_availability       : dict[UUID, models.ProductAvailability] = None
    product_images             : dict[UUID, models.ProductImage]        = None
    product_requests_received  : dict[UUID, models.ProductRequest]      = None
    product_requests_submitted : dict[UUID, models.ProductRequest]      = None
    payout_accounts            : dict[UUID, models.PayoutAccount]       = None
    balance_transfers          : dict[UUID, models.BalanceTransfer]     = None






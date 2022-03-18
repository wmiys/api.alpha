#************************************************************************************
#
#                           Product Search Request
#
# The product search request is responsible for handling all of the product search requests.
#
#
#************************************************************************************

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from ...common import sorting
from ...common import pagination

    
@dataclass
class ProductSearchRequest:
    location_id: int                    = None
    starts_on   : datetime              = None
    ends_on     : datetime              = None
    sorting     : sorting.Sorting       = None
    pagination  : pagination.Pagination = None
"""
**********************************************************************************************
Domain model for a product availability
**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date

@dataclass
class ProductListingAvailability:
    product_id  : int  = None
    location_id : int  = None
    starts_on   : date = None
    ends_on     : date = None







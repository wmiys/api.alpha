"""
**********************************************************************************************
A product listing availability has 1 responsibility: checking if the given product is available
to rent given the parms.
**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class ProductListingAvailability:
    product_id  : int = None
    location_id : int = None
    starts_on   : str = None
    ends_on     : str = None







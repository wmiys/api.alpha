"""
**********************************************************************************************
A product availability record represents a lender provided date range that they do not wish for
their product to be available for rent. 

So renters will not be able to see the product in the search results if their start/end date range
conflicts with any product availability record.

Furthermore, products that have conflicting availability records will not be able to even receive 
requests from renters if the starts/ends range conflicts.
**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProductAvailability:
    id         : int      = None
    product_id : int      = None
    starts_on  : datetime = None
    ends_on    : datetime = None
    note       : str      = None
    created_on : datetime = None
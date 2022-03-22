"""
**********************************************************************************************
A location is used to pin point an address. 

Lenders give their products a location value. This determines how far out they are willing
to drop off their products to a renter. Or, lenders' products will only show up in the search
results if their product's location and dropoff distance fall within the searchers dropoff 
location.
**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Location:
    id        : int = None
    city      : str = None
    state_id  : str = None
    state_name: str = None


        

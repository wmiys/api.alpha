"""
**********************************************************************************************
A product listing represents a product that is publicly visible to all renters. This is what
data is used when a renter goes to a product-listing page. 

It's essentially the same thing as the product view from the lender's side.

I just thought it would be a good idea to seperate out the views for security... might have been a mistake.
**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ProductListing:
    product_id: int=None


    

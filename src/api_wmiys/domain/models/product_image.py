"""
**********************************************************************************************
A product image represents a single additional image given to a product (not the cover photo).

Currently, the only way to update the images for a product is by first deleting all of them,
then you can post a list of new ones.

This will need to be updated soon.
**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProductImage:
    id         : int      = None
    product_id : int      = None
    file_name  : str      = None
    created_on : datetime = None
            


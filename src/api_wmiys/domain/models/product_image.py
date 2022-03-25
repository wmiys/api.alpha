"""
**********************************************************************************************

Product Image domain model.

**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class ProductImage:
    id         : UUID      = None
    product_id : int      = None
    file_name  : str      = None
    created_on : datetime = None
            


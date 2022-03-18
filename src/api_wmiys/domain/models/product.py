#************************************************************************************
#
#                           Product Class
#
#************************************************************************************
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Product:
    """Product domain model"""
    
    id                        : int      = None
    user_id                   : int      = None
    name                      : str      = None
    description               : str      = None
    product_categories_sub_id : int      = None
    location_id               : int      = None
    dropoff_distance          : str      = None
    price_full                : float    = None
    image                     : str      = None
    minimum_age               : int      = None
    created_on                : datetime = None



        
        









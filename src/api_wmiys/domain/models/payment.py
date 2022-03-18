"""
**********************************************************************************************
This class represents a payment record in the database.

payment_session_id represents the session_id generated from the stripe API.

A payment occurs when a renter finds a product that they want to rent, and they have successfully
gave stripe their card information and it was successfully charged.
**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Payment:
    id                  : UUID     = None
    product_id          : int      = None
    renter_id           : int      = None
    dropoff_location_id : int      = None
    starts_on           : datetime = None
    ends_on             : datetime = None
    price_full          : float    = None
    fee_renter          : float    = None
    fee_lender          : float    = None
    created_on          : datetime = None




    












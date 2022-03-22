"""
**********************************************************************************************
Product requests are what the name implies... a renter has found a listing that is available
during the given start/end range, the renter has successfully paid for the product rental with stripe
and we have collected the funds. Now, the lender needs to finally approve the product rental with 
the renter.

Initially, a request status is set to 'pending'. The lender has 24 hours to respond to the 
request before being marked as 'expired' and the renter is fully refunded (and the request
cannot be responded to). Lenders can respond to a requests by either accepting or denying them.

Once a request status is either responded to or it expires, lenders cannot update a request.
**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


#-----------------------------------------------------
# Possible product request status values
# ----------------------------------------------------
class RequestStatus(str, Enum):
    pending  = 'pending'
    accepted = 'accepted'
    denied   = 'denied'
    expired  = 'expired'


#-----------------------------------------------------
# Product Request class
# ----------------------------------------------------
@dataclass
class ProductRequest:
    id           : UUID          = None
    payment_id   : UUID          = None
    session_id   : str           = None
    status       : RequestStatus = RequestStatus.pending
    responded_on : datetime      = None
    created_on   : datetime      = None
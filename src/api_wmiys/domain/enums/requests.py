"""
**********************************************************************************************

Enums related to the ProductRequest domain model

**********************************************************************************************
"""

from __future__ import annotations
from enum import Enum

#-----------------------------------------------------
# Possible product request status values
# ----------------------------------------------------
class RequestStatus(str, Enum):
    PENDING  = 'pending'
    ACCEPTED = 'accepted'
    DENIED   = 'denied'
    EXPIRED  = 'expired'
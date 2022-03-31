"""
**********************************************************************************************

Product Request domain model

**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from api_wmiys.domain.enums.requests import RequestStatus


#-----------------------------------------------------
# Product Request class
# ----------------------------------------------------
@dataclass
class ProductRequest:
    id           : UUID          = None
    payment_id   : UUID          = None
    session_id   : str           = None
    status       : RequestStatus = RequestStatus.PENDING
    responded_on : datetime      = None
    created_on   : datetime      = datetime.now()
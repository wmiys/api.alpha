"""
**********************************************************************************************

Product Request domain model

**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from api_wmiys.domain.enums.product_requests import RequestStatus
from api_wmiys.domain.models.user import User
from api_wmiys.domain.models.payment import Payment


#-----------------------------------------------------
# Product Request class
# ----------------------------------------------------
@dataclass
class ProductRequest:
    id             : UUID          = None
    payment_id     : UUID          = None
    session_id     : str           = None
    status         : RequestStatus = RequestStatus.PENDING
    responded_on   : datetime      = None
    review_score   : int           = None
    review_comment : str           = None
    created_on     : datetime      = datetime.now()


#-----------------------------------------------------
# Internal product request model
#
# It has everything that the ProductRequest model has, 
# plus all the info about the lender and renter.
#-----------------------------------------------------
@dataclass
class ProductRequestInternal(ProductRequest):
    renter     : User    = None
    lender     : User    = None
    payment    : Payment = None
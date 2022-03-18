"""
**********************************************************************************************
Payout Accounts represent the lender's connected account on stripe. 

Before users can start lending their products, they need to setup an account with stripe.

This is so we can pay out their account balance to their bank account after successfully 
lending out their products. 
**********************************************************************************************
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class PayoutAccount:
    id         : UUID     = None
    user_id    : int      = None
    account_id : str      = None
    created_on : datetime = None
    confirmed  : bool     = False


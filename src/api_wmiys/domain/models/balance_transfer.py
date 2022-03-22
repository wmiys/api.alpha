"""
**********************************************************************************************
This class represents a balance transfer. 
Balance transfers occur when a lender wants to transfer their earnings to their bank account.
Lenders need to have a balance greater than 1 in order to successfully transfer their balance.
**********************************************************************************************
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class BalanceTransfer:
    id                     : UUID     = None
    user_id                : int      = None
    amount                 : float    = 0
    created_on             : datetime = None
    destination_account_id : str      = None
    transfer_id            : str      = None
"""
**********************************************************************************************

Represents a password reset object. 

**********************************************************************************************
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class PasswordReset:
    id          : UUID     = None
    email       : str      = None
    created_on  : datetime = None
    password    : str      = None
    updated_on  : datetime = None




    

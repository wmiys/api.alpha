#************************************************************************************
#
# This class handles all the requests for a single user.
#
#************************************************************************************

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id         : int      = None
    email      : str      = None
    password   : str      = None
    name_first : str      = None
    name_last  : str      = None
    birth_date : datetime = None
    created_on : datetime = None






        


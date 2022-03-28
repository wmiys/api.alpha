"""
**********************************************************************************************

The base return class.
Used for returning data from a function.

**********************************************************************************************
"""



from dataclasses import dataclass
from typing import Any


@dataclass
class BaseReturn:
    successful : bool      = None
    data       : Any       = None
    error      : Exception = None

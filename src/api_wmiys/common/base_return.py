"""
**********************************************************************************************

The base return class.
Used for returning data from a function.

**********************************************************************************************
"""


from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseReturn:
    successful : bool      = None
    data       : Any       = None
    error      : Exception = None


@dataclass
class FilteredDataReturn(BaseReturn):
    data          : list[dict] = None
    count_records : int        = 0
    count_pages   : int        = 0

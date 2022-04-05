"""
**********************************************************************************************

Seach locations domain model

**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass
from api_wmiys.domain.enums.search_locations import PerPageLimits


@dataclass
class SearchLocations:
    query    : str = None
    per_page : int = PerPageLimits.DEFAULT.value





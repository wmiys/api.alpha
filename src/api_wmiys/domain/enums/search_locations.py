"""
**********************************************************************************************

Search locations enums and symbolic constants.

**********************************************************************************************
"""

from __future__ import annotations
from enum import Enum

#------------------------------------------------------
# Per page url parm range and default
#------------------------------------------------------
class PerPageLimits(Enum):
    DEFAULT = 20
    MAX     = 100
    MIN     = 1
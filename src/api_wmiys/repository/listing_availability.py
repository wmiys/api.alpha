"""
**********************************************************************************************

Product listing availability sql commands.

**********************************************************************************************
"""

from __future__ import annotations
import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models


SQL_SELECT = '''
    SELECT 
        SEARCH_PRODUCTS_FILTER(%s, %s, %s, %s) AS result;
'''


#------------------------------------------------------
# Checks if the product is available during the dates and location
#
# Returns a bool:
#   true - product is available
#   false - product is not available
#------------------------------------------------------ 
def select(model: models.ProductListingAvailability) -> DbOperationResult:
    parms = (
        model.product_id, 
        model.location_id, 
        model.starts_on, 
        model.ends_on,
    )

    return sql_engine.select(SQL_SELECT, parms)
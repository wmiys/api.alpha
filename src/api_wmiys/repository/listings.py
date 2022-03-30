"""
**********************************************************************************************

Product listing sql commands.

**********************************************************************************************
"""

from __future__ import annotations
import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models


SQL_SELECT = '''
    SELECT 
        * 
    FROM 
        View_Product_Listings vpl
    WHERE 
        vpl.id = %s
    LIMIT 1;
'''

#----------------------------------------------------------
# Select the product record from the View_Product_Listings table.
#----------------------------------------------------------
def select(product_id) -> DbOperationResult:
    parms = (product_id,)
    return sql_engine.select(SQL_SELECT, parms)
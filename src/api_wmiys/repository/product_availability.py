
from __future__ import annotations

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models


SQL_SELECT_ALL = """
    SELECT   *
    FROM     View_Product_Availability pa
    WHERE    pa.product_id = %s
    ORDER BY pa.created_on DESC;
"""


#------------------------------------------------------
# Returns all product availability records for a single product
#
# Parms:
#   product_id - the product id
#
# Returns: list of product availability records
#------------------------------------------------------
def selectAll(product_id) -> DbOperationResult:
    parms = (product_id,)
    return sql_engine.selectAll(SQL_SELECT_ALL, parms)
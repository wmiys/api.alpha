"""
**********************************************************************************************

SQL commands for received product requests submitted (as the renter).

**********************************************************************************************
"""

from __future__ import annotations
from uuid import UUID
import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain.enums.product_requests import RequestStatus



_SQL_SELECT_ALL_TEMPLATE = '''
    SELECT 
        * 
    FROM 
        View_Requests_Renter v 
    WHERE 
        v.renter_id = %s 
        {status_filter} 
    ORDER BY 
        v.created_on DESC;
'''

SQL_SELECT_ALL           = _SQL_SELECT_ALL_TEMPLATE.format(status_filter='')
SQL_SELECT_ALL_BY_STATUS = _SQL_SELECT_ALL_TEMPLATE.format(status_filter='AND v.status = %s')


SQL_SELECT = '''
    SELECT 
        * 
    FROM 
        View_Requests_Renter v 
    WHERE 
        v.id = %s
    LIMIT 
        1;
'''



#-----------------------------------------------------
# Retrieve all the requests that a renter has submitted.
# 
# Parms:
#   renter_id: the renter's user id
# ----------------------------------------------------
def selectAll(renter_id) -> DbOperationResult:
    parms = (renter_id,)
    return sql_engine.selectAll(SQL_SELECT_ALL, parms)


#-----------------------------------------------------
# Retrieve all the requests that a renter has submitted
# that have the specified status.
# 
# Parms:
#   renter_id: the renter's user_id
#   status: the status to filter by
# ----------------------------------------------------
def selectAllByStatus(renter_id, status: RequestStatus) -> DbOperationResult:
    parms = (
        renter_id,
        status.value,
    )

    return sql_engine.selectAll(SQL_SELECT_ALL_BY_STATUS, parms)


#-----------------------------------------------------
# Retrieve a single submitted product request
# 
# Parms:
#   product_request_id: the product request's id
# ----------------------------------------------------
def select(product_request_id: UUID) -> DbOperationResult:
    parms = (
        str(product_request_id),
    )
    return sql_engine.select(SQL_SELECT, parms)
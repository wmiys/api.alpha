"""
**********************************************************************************************

SQL commands for received product requests.

**********************************************************************************************
"""

from __future__ import annotations
import pymysql.commands as sql_engine
from pymysql.connection import ConnectionPrepared
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models
from api_wmiys.domain.enums.requests import RequestStatus

_SQL_SELECT_ALL_TEMPLATE = '''
    SELECT
        v.*
    FROM
        View_Requests_Lender v
    WHERE
        EXISTS (
            SELECT
                1
            FROM
                Products p
            WHERE
                p.id = v.product_id
                AND p.user_id = %s 
                {status_clause}
        )
    ORDER BY
        v.created_on DESC;
'''

SQL_SELECT_ALL = _SQL_SELECT_ALL_TEMPLATE.format(status_clause='')
SQL_SELECT_ALL_BY_STATUS = _SQL_SELECT_ALL_TEMPLATE.format(status_clause=' AND v.status = %s ')


#-----------------------------------------------------
# Retrieve all the requests that a lender has received.
# 
# Parms:
#   lender_id - the lender's user_id
# ----------------------------------------------------
def selectAll(lender_id) -> DbOperationResult:
    parms = (lender_id,)
    return sql_engine.selectAll(SQL_SELECT_ALL, parms)


#-----------------------------------------------------
# Retrieve all the requests that a lender has received
# that have the specified status.
# 
# Parms:
#   lender_id: the lender's user_id
#   status: the status to filter by
# ----------------------------------------------------
def selectAllByStatus(lender_id, status: RequestStatus) -> DbOperationResult:
    parms = (
        lender_id,
        status.value,
    )

    return sql_engine.selectAll(SQL_SELECT_ALL_BY_STATUS, parms)
"""
**********************************************************************************************

SQL commands for received product requests.

**********************************************************************************************
"""

from __future__ import annotations
from uuid import UUID
import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models
from api_wmiys.domain.enums.product_requests import RequestStatus


SQL_SELECT = '''
    SELECT 
        pr.id as id,
        pr.payment_id as payment_id,
        pr.session_id as session_id,
        pr.status as status,
        pr.responded_on as responded_on,
        pr.created_on as created_on
    FROM 
        Product_Requests pr
    WHERE 
        pr.id = %s
    LIMIT 
        1;
'''



def select(request_id: UUID) -> DbOperationResult:
    parms = (str(request_id),)
    return sql_engine.select(SQL_SELECT, parms)

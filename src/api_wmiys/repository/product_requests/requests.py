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



VIEW_NAME = 'View_Product_Requests_Internal'

SQL_SELECT = f'''
    SELECT 
        *
    FROM 
        {VIEW_NAME} pr
    WHERE
        pr.product_request_id = %s
    LIMIT 
        1;
'''


def select(product_request_id: UUID) -> DbOperationResult:
    parms = (str(product_request_id),)
    return sql_engine.select(SQL_SELECT, parms)


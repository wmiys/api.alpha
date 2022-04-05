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


SQL_MODIFY = '''
    INSERT INTO
        Product_Requests (id, payment_id, session_id, status, responded_on)
    VALUES
        (%s, %s, %s, %s, %s) AS new_values 
    ON DUPLICATE KEY UPDATE
        status       = new_values.status,
        responded_on = new_values.responded_on;
'''

#-----------------------------------------------------
# select a single product request record from the internal table
#-----------------------------------------------------
def select(product_request_id: UUID) -> DbOperationResult:
    parms = (str(product_request_id),)
    return sql_engine.select(SQL_SELECT, parms)

#-----------------------------------------------------
# Update an existing product request record
#-----------------------------------------------------
def update(product_request: models.ProductRequest) -> DbOperationResult:
    return _modify(product_request)

#-----------------------------------------------------
# Insert a new product request record
#-----------------------------------------------------
def insert(product_request: models.ProductRequest) -> DbOperationResult:
    return _modify(product_request)

#-----------------------------------------------------
# Insert or update a product request record
#-----------------------------------------------------
def _modify(product_request: models.ProductRequest) -> DbOperationResult:
    parms = _getModifyParms(product_request)
    return sql_engine.modify(SQL_MODIFY, parms)

#-----------------------------------------------------
# Get the parms tuple for the modify command
#-----------------------------------------------------
def _getModifyParms(product_request: models.ProductRequest) -> tuple:
    parms = (
        str(product_request.id),
        str(product_request.payment_id),
        product_request.session_id,
        product_request.status.value,
        product_request.responded_on,
    ) 

    return parms





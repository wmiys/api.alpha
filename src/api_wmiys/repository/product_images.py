"""
**********************************************************************************************

All the SQL commands for the Product_Images table.

**********************************************************************************************
"""

from __future__ import annotations
import pymysql.commands as sql_engine
from pymysql.connection import ConnectionPrepared
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models


SQL_INSERT = '''
    INSERT INTO 
        Product_Images (id, product_id, file_name, created_on)
    VALUES
        (%s, %s, %s, %s);
'''

SQL_SELECT_ALL = '''
    SELECT   
        *
    FROM     
        Product_Images pi
    WHERE    
        pi.product_id = %s;
'''


SQL_DELETE_ALL = 'DELETE FROM Product_Images WHERE id = %s;'


#----------------------------------------------------------
# Insert the product images into the database
#----------------------------------------------------------
def insertBatch(product_images: list[models.ProductImage]) -> DbOperationResult:
    parms = _getInsertBatchTuples(product_images)
    return _executeManyCommand(SQL_INSERT, parms)


#-----------------------------------------------------
# Get a list of parameter tuples to use for the batch insert command
#-----------------------------------------------------
def _getInsertBatchTuples(product_images: list[models.ProductImage]) -> list[tuple]:
    tuples = []

    for product_image in product_images:
        parm = _getInsertParmTuple(product_image)
        tuples.append(parm)

    return tuples


#-----------------------------------------------------
# Get a paramter tuple for the given ProductImage object
#-----------------------------------------------------
def _getInsertParmTuple(product_image: models.ProductImage) -> tuple:
    parms = (
        str(product_image.id),
        product_image.product_id,
        product_image.file_name,
        product_image.created_on,
    )

    return parms

#----------------------------------------------------------
# Delete all the product images for a product
#----------------------------------------------------------
def deleteAll(product_images: list[models.ProductImage]) -> DbOperationResult:
    parms = _getDeleteBatchTuples(product_images)
    return _executeManyCommand(SQL_DELETE_ALL, parms)


#-----------------------------------------------------
# Get a list of parameter tuples to use for the batch delete command
#-----------------------------------------------------
def _getDeleteBatchTuples(product_images: list[models.ProductImage]) -> list[tuple]:
    tuples = []

    for p in product_images:
        tuples.append((str(p.id),))
    
    return tuples

#-----------------------------------------------------
# Perform a executemany command with the given sql statement and parm list
#-----------------------------------------------------
def _executeManyCommand(sql_stmt: str, parms: list[tuple]) -> DbOperationResult:
    result = DbOperationResult(successful=True)

    db = ConnectionPrepared()
    db.connect()
    cursor = db.getCursor()

    try:    
        cursor.executemany(sql_stmt, parms)
        db.commit()
        result.data = cursor.rowcount
    except Exception as e:
        result.error = e
        result.successful = False

    finally:
        db.close()

    return result


#----------------------------------------------------------
# Retrieve all the product image database records that belong
# to the given product.
#----------------------------------------------------------
def selectAll(product_id) -> DbOperationResult:
    parms = (product_id,)
    return sql_engine.selectAll(SQL_SELECT_ALL, parms)



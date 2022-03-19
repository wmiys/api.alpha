from __future__ import annotations

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from pymysql.connection import ConnectionPrepared
from api_wmiys.domain import models

#------------------------------------------------------
# Select all products
# 
# Parms:
#   user_id
#------------------------------------------------------
SQL_SELECT_ALL = """
    SELECT  *
    FROM    View_Products p
    WHERE   p.user_id = %s
    GROUP   BY p.id
    ORDER   BY p.name ASC;
"""

#------------------------------------------------------
# Select a single product
# 
# Parms:
#   product id
#   user id
#------------------------------------------------------
SQL_SELECT = """
    SELECT  *
    FROM    View_Products p
    WHERE   p.id = %s
    AND     p.user_id = %s
    GROUP   BY p.id
    LIMIT   1;
"""

#------------------------------------------------------
# Insert a new product
# 
# Parms:
#   - user_id,
#   - name
#   - description,
#   - product_categories_sub_id
#   - location_id
#   - dropoff_distance
#   - price_full
#   - image
#   - minimum_age
#------------------------------------------------------
SQL_INSERT = """
    INSERT INTO Products
    (user_id, name, description, product_categories_sub_id, location_id, dropoff_distance, price_full, image, minimum_age) VALUES
    (%s,      %s,   %s,          %s,                        %s,          %s,               %s,         %s,    %s);
"""


#------------------------------------------------------
# Retrieve all the user's products
#------------------------------------------------------
def selectAll(user_id) -> DbOperationResult:
    parms = (user_id,)
    return sql_engine.selectAll(SQL_SELECT_ALL, parms)



def select(product: models.Product) -> DbOperationResult:
    parms = (product.id, product.user_id)
    return sql_engine.select(SQL_SELECT, parms)


#------------------------------------------------------
# Insert the given product into the database
#------------------------------------------------------
def insert(product: models.Product) -> DbOperationResult:
    result = DbOperationResult(successful=True)
    db = ConnectionPrepared()
    parms = _getInsertParms(product)

    try:
        db.connect()
        cursor = db.getCursor()
        cursor.execute(SQL_INSERT, parms)
        db.commit()
        
        result.data = cursor.rowcount
        product.id = cursor.lastrowid
    except Exception as e:
        result.error = e
        result.data = None
        result.successful = False
    finally:
        db.close()
    
    return result

#------------------------------------------------------
# Retrieve the parms tuple needed for the insert statement
#------------------------------------------------------
def _getInsertParms(product: models.Product) -> tuple:
    parms = (
        product.user_id,                   product.name,          product.description, 
        product.product_categories_sub_id, product.location_id,   product.dropoff_distance, 
        product.price_full,                product.image,         product.minimum_age
    )

    return parms
    
